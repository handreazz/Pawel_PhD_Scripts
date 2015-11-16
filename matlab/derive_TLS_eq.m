syms x y z;
r = [x; y; z];
rt = transpose(r);

syms T11 T12 T13 T22 T23 T33;
T = [T11 T12 T13;
     T12 T22 T23;
     T13 T23 T33];

syms L11 L12 L13 L22 L23 L33;
L = [L11 L12 L13;
     L12 L22 L23;
     L13 L23 L33];

syms S11 S12 S13 S21 S22 S23 S31 S32 S33;
S = [S11 S12 S13;
     S21 S22 S23;
     S31 S32 S33];
St=transpose(S); 

syms x1 y1 z1;
r1 = [x1; y1; z1];
syms x2 y2 z2;
r2t = [x2 y2 z2];




uikuil = T + TLS_cross(St,rt) - TLS_cross(r, S) - TLS_cross(r, TLS_cross(L,rt))   

uiui = trace(uikuil)

UikUjl = T + TLS_cross(St,r2t) - TLS_cross(r1,S) - TLS_cross(r1, TLS_cross(L,r2t))

uiuj = trace(UikUjl)