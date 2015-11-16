#!/usr/bin/awk -f
BEGIN{
 N  = 512   # number of molecules
 T  = 310.0 # temperature
 H1 = 0.0   # 1st moment of enthalpy (E+pV)
 H2 = 0.0   # 2nd moment of enthalpy
 HV = 0.0   # enthalpy/volume moment (E+pV)*V
 V  = 0.0   # volume
 N  = 0     # samples
 kB = 1.3801*6.022/4184                      # in kcal/mol-K
 atmA3_2_kcalmol = 101325*6.022*10^(-7)/4184 # convert PV to kcal/mol
 dEvib_dT = -2.1313 # correction for internal vibrations in cal/mol-K
}
{
 if(NF == 12){  #i.e. this is not a comment line
   N++
   H1 += ($2 + $7*atmA3_2_kcalmol)
   H2 += ($2 + $7*atmA3_2_kcalmol)^2
   HV += ($2 + $7*atmA3_2_kcalmol)*$7
   V  += $7
 }
}
END{
  H1 /= N
  H2 /= N
  HV /= N
  V  /= N
  Hvar    = H2 - H1*H1
  Cp      = Hvar / (N*kB*T)*1000 + dEvib_dT
  alpha_p = (HV - V*H1) / (kB*T*T*V) * 10000
  printf(" H  = % 13.6f +/- %13.6f (kcal/mol)\n Cp = % 13.6f (cal/mol-K) alpha_p = %13.6f (K-1 * 10^-4)\n ",H1,sqrt(Hvar),Cp,alpha_p)
}
