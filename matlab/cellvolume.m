%drata is the name of the rst or inpcrd file which has the box dimensions at the end
function volume = cellvolume(drata)
    A=importdata(drata,' ',2);
    gdim=A.data(end,:);
    gdim(4:6)=gdim(4:6)*pi/180.0;
    dx = cos(gdim(5))*cos(gdim(6)) - cos(gdim(4));
    dx = dx / (sin(gdim(5)) * sin (gdim(6)));
    dy = sqrt(1.0 - dx*dx);
    invU = zeros(3,3);
    invU(1,1) = gdim(1);
    invU(1,2) = gdim(2)*cos(gdim(6));
    invU(1,3) = gdim(3)*cos(gdim(5));
    invU(2,2) = gdim(2)*sin(gdim(6));
    invU(2,3) = -gdim(3)*sin(gdim(5))*dx;
    invU(3,3) = gdim(3)*sin(gdim(5))*dy;
    U = inv(invU);
    volume=invU(1,1)*invU(2,2)*invU(3,3);
end
