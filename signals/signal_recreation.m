on = [ones(1,33)*1.5 ones(1,15)*(-4)];
off = [ones(1,13)*1.5 ones(1,35)*(-4)];
header = ones(1,100)*-4;
wait = zeros(1,5199);

max_alt = [header on on off on on on on on on off off off on off off off off on off off off off off off off off off  off on off on off];
max_alt_with_wait = [max_alt wait];
two_maxes = [max_alt_with_wait max_alt_with_wait max_alt_with_wait];

t = 1:length(max_alt);

x = wavread('max_0_0.wav');
x = x(:,1)*100;

% This was found by manually looking at the signal
x_signal_start = 8265;

figure(1);
plot(t,x(x_signal_start:(x_signal_start+length(max_alt)-1)),t,max_alt);

x_signal_start = 88265;
s = repmat(max_alt_with_wait,1,120);
s = s';
t1 = 80000:length(s);
length(t1)

figure(2);
plot(t1,x(x_signal_start:x_signal_start+length(t1)-1),t1,s(80000:length(s)))

wavwrite(s./100,44100,'max_0_0_sim.wav');

sound(s,44100);