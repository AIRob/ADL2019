import torch
import torch.nn.functional as F

class CosAttentionsMaxNet(torch.nn.Module):
    """
    Args:
    """

    def __init__(self, dim_embeddings,
                 similarity='CosineSimilarity'):
        super(CosAttentionsMaxNet, self).__init__()
        self.hidden_size = 128
        self.num_layers = 1
        self.rnn = torch.nn.GRU(dim_embeddings, self.hidden_size, self.num_layers, batch_first=True, bidirectional=True)
        self.attention_rnn = torch.nn.GRU((self.hidden_size * 2) * 2, self.hidden_size, self.num_layers, batch_first=True, bidirectional=True)
 
    def forward(self, context, context_lens, options, option_lens):
        context_length = context.size(1)

        # Set initial hidden and cell states 
        h_0 = torch.zeros(self.num_layers * 2, context.size(0), self.hidden_size).to(context.get_device())
        
        # Forward propagate RNN
        # context_outs: tensor of shape (batch, context_length, hidden_size * 2)
        # context_h_n: tensor of shape (num_layers * 2, batch, hidden_size)
        context_outs, context_h_n = self.rnn(context, h_0)

        logits = []
        for i, option in enumerate(options.transpose(1, 0)):
            option_length = option.size(1)

            # Set initial hidden and cell states 
            h_0 = torch.zeros(self.num_layers * 2, context.size(0), self.hidden_size).to(context.get_device())

            # Forward propagate RNN
            # option_outs: tensor of shape (batch, option_length, hidden_size * 2)
            # option_h_n: tensor of shape (num_layers * 2, batch, hidden_size)
            option_outs, option_h_n = self.rnn(option, h_0)
            
            # repeat_context_outs: tensor of shape (batch, context_length, hidden_size * 2) -> (batch, option_length, context_length, hidden_size * 2)
            repeat_context_outs = torch.unsqueeze(context_outs, 1).repeat((1, option_length, 1, 1))
            # repeat_option_outs: tensor of shape (batch, option_length, hidden_size * 2) -> (batch, option_length, context_length, hidden_size * 2)
            repeat_option_outs = torch.unsqueeze(option_outs, 2).repeat((1, 1, context_length, 1))
            # attentions: tensor of shape (batch, option_length, context_length, hidden_size * 2) -> (batch, option_length, context_length)
            attentions = torch.nn.CosineSimilarity(dim=-1)(repeat_context_outs, repeat_option_outs)
            
            # # attention_context: tensor of shape (batch, context_length, option_length) x (batch, option_length, hidden_size * 2) -> (batch, context_length, hidden_size * 2)
            attention_context = torch.bmm(F.softmax(attentions, dim=1).transpose(1, 2), option_outs)
            # attention_option: tensor of shape (batch, option_length, context_length) x (batch, context_length, hidden_size * 2) -> (batch, option_length, hidden_size * 2)
            attention_option = torch.bmm(F.softmax(attentions, dim=2), context_outs)

            # Set initial hidden and cell states 
            h_1 = torch.zeros(self.num_layers * 2, context.size(0), self.hidden_size).to(context.get_device())

            # Forward propagate RNN
            # attention_context_outs: tensor of shape (batch, context_length, hidden_size * 2)
            # attention_context_h_n: tensor of shape (num_layers * 2, batch, hidden_size)
            attention_context_outs, attention_context_h_n = self.attention_rnn(torch.cat((attention_context, context_outs), dim=-1), h_1)

            # Max pooling over RNN outputs.
            # attention_context_outs_max: tensor of shape (batch, hidden_size * 2)
            attention_context_outs_max = attention_context_outs.max(dim=1)[0]

            # Set initial hidden and cell states 
            h_1 = torch.zeros(self.num_layers * 2, option.size(0), self.hidden_size).to(option.get_device())

            # Forward propagate RNN
            # attention_option_outs: tensor of shape (batch, option_length, hidden_size * 2)
            # attention_option_h_n: tensor of shape (num_layers * 2, batch, hidden_size)
            attention_option_outs, attention_option_h_n = self.attention_rnn(torch.cat((attention_option, option_outs), dim=-1), h_1)

            # attention_option_h: tensor of shape (num_layers * 2, batch, hidden_size) -> (batch, num_layers * 2, hidden_size)
            attention_option_h = attention_option_h_n.transpose(1, 0)
            # Flatten the hidden states of the last time step -> (batch, num_layers * 2 * hidden_size)
            attention_option_h = attention_option_h.contiguous().view(option.size(0), -1)

            # Max pooling over RNN outputs.
            # attention_option_outs_max: tensor of shape (batch, hidden_size * 2)
            attention_option_outs_max = attention_option_outs.max(dim=1)[0]

            # Cosine similarity between context and each option.
            logit = torch.nn.CosineSimilarity(dim=1)(attention_context_outs_max, attention_option_outs_max)
            logits.append(logit)

        logits = F.softmax(torch.stack(logits, 1), dim=1)
        return logits