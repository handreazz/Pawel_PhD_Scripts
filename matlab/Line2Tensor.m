%Convert a 1x6 line into a 3x3 tensor (for example Ucif or Anisou record)
%to the corresponding anisotropic tensor

function tensor=Line2Tensor(line)

tensor =[line(1) line(4) line(5); line(4) line(2) line(6); line(5) line(6) line(3)];