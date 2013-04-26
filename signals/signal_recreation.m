
on = [ones(1,33)*1.5 ones(1,15)*(-4)];
off = [ones(1,13)*1.5 ones(1,35)*(-4)];
header = ones(1,100)*-4;
wait = zeros(1,5199);

sig =   [on on on on on on on on on off off off on off off off off on off off off off off off off off off off on on off off];

max_alt = [header sig];
max_alt_with_wait = [max_alt wait];
s = repmat(max_alt_with_wait,1,32);
s = s';

sig1 =  [on on on on on on on on off off off off on off off off off on off off off off off off on on on on off on off off];

max_alt = [header sig];
max_alt_with_wait = [max_alt wait];
s2 = repmat(max_alt_with_wait,1,1);
s2 = s2';

s = [s;s2;s];

%{
two_maxes = [max_alt_with_wait max_alt_with_wait max_alt_with_wait];

t = 1:length(max_alt_with_wait);

x = wavread('max_0_0.wav');
x = x(:,1)*100;

% This was found by manually looking at the signal
x_signal_start = 8265;

figure(1);
plot(t,x(x_signal_start:(x_signal_start+length(max_alt_with_wait)-1)),t,max_alt_with_wait);
%plot(t,x(x_signal_start:(x_signal_start+length(max_alt_with_wait)-1)));


x_signal_start = 88265;
t1 = 80000:length(s);

figure(2);
plot(t1,x(x_signal_start:x_signal_start+length(t1)-1),t1,s(80000:length(s)));
%}
wavwrite(s./100,44100,'max_0_0_sim.wav');

sound(s,44100);