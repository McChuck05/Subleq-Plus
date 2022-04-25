 # Subleq+ Parser
 # Copyright (C) 2022 McChuck
 # original Copyright (C) 2013 Chris Lloyd
 # Released under GNU General Public License
 # See LICENSE for more details.
 # https://github.com/cjrl
 # lloyd.chris@verizon.net

 #  A B C    [B] -= [A], if [B]<=0 goto C
 #  A B      A B ?  (B -= A, goto next)
 #  A        A A ?  (A = 0, goto next)
 #  A !      print [A], goto next
 #  ! B      input [B], goto next
 #  A A !    halt
 #  A *B *C  [[B]] -= [A], if [[B]]<=0 goto [C]

 #  ?        next address
 #  @        this address
 #  label:   address label, cannot be the only thing on a line
 #  *label   pointer to address label, represented as a negative address
 #  !        -1 used for input, output, and halting (use 0 for noecho input)
 #  ;        end of instruction
 #  #        comment
 #  .        data indicator
 #  " or '   string delimeters, must be data


class SubleqpParser:

    tokens = []
    label_table = {}

    def parse(self,string):
        string = self.expand_literals(string)
        string = string.replace('\n',';')
        string = string.replace('#',';#')
        string = string.replace(':',': ')
        string = string.replace('.','. ')
        string = string.replace('!', "-1 ")
        string.replace('@', '@ ')
        string.replace('?', '? ')
        self.tokens = [token.split() for token in string.split(';') if not '#' in token and token.strip()]
        self.parse_labels()
        self.expand_instructions()
        self.update_labels()
        self.tokens = [token for token in sum(self.tokens,[]) if token != '.']
        self.resolve_labels();
        try:
            response = []
            for token in self.tokens:
                response.append(int(token))
            return(response)
        except ValueError:
            print("Unmatched label:", token, flush=True)
            raise

    def resolve_labels(self):
        for i, token in enumerate(self.tokens):
            if token[0] == "*":     # pointer
                token = token[1:]
                if token in self.label_table:
                    self.tokens[i] = -(self.label_table[token])
            else:
                if token in self.label_table:
                    self.tokens[i] = self.label_table[token]
                if token == '?':
                    self.tokens[i] = i+1
                if token == '@':
                    self.tokens[i] = i


    def update_labels(self):
        for i, label in enumerate(self.label_table):
            self.label_table[label] = self.get_label_index(label)

    def get_label_index(self,label):
        index = 0
        address, x = self.label_table[label]
        for i in range(address):
            index += len(self.tokens[i])
            if '.' in self.tokens[i][0]:
                index -= 1 
        if '.' in self.tokens[address][0]:
            return index + x - 1
        return index

    def expand_instructions(self):
        for token_index, token in enumerate(self.tokens):
            if not token[0] == '.':
                oprands = [token[0],token[0],'?']
                for i, oprand in enumerate(token):
                    oprands[i] = oprand
                self.tokens[token_index] = oprands

    def parse_labels(self):
        for token_index, token in enumerate(self.tokens):
            for oprand_index, oprand in enumerate(token):
                if ':' in oprand:
                    token.remove(oprand)
                    self.label_table[oprand[:-1]] = (token_index,oprand_index) 

    def expand_literals(self,string):
        in_dq_literal = False       # "
        in_sq_literal = False       # '
        expanded_string = ""
        for char in string:
            if char == '"' and not in_sq_literal:
                in_dq_literal ^= True
            elif char == "'" and not in_dq_literal:
                in_sq_literal ^= True
            elif in_dq_literal or in_sq_literal:
                expanded_string += str(ord(char)) + ' '
            else:
                expanded_string += char
        return expanded_string
