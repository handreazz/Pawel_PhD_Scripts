function DiffConst =test(netcdffile)
ncid = netcdf.open(netcdffile,'NC_NOWRITE')
[ndims,nvars,natts,unlimdimID]= netcdf.inq(ncid)
[varname, vartype, dimids, natts] = netcdf.inqVar(ncid,2)
coordinates = netcdf.getVar(ncid,2);
lastframe=coordinates(:,9793:10224,12620); %change to give selected atoms and last frame in trajectory
firstframe=coordinates(:,9793:10224,1);

SD=zeros(432,3); %change 1st number to number of atoms
for i = 1:432
    for j = 1:3
        SD(i,j)=(lastframe(j,i)-firstframe(j,i))^2;
    end
end

xMSD=mean(SD(:,1))
yMSD=mean(SD(:,2))
zMSD=mean(SD(:,3))
totMSD=xMSD+yMSD+zMSD
DiffConst=totMSD/252400*10/6 %2000 is the time in picoseconds