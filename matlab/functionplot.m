syms r
k=1
a=1
l=1
m=1
y=(k/r^2)*exp(-r/a)
z=(l^2/(2*m*r^2))
v=y+z
h1=ezplot(z,[0,10])
hold on
h2=ezplot(y,[0,10])
h3=ezplot(v,[0,10])
set(h1, 'Color', 'm');
set(h3, 'Color', 'k');