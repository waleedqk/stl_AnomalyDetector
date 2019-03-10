Globally, it is always the case that if x == 0 holds, then y == 1 holds after at most 6 time unit(s).

    G(x == 0 -> F[0,6](y == 1))

Globally, its always the case that x == 0 holds at least every 10 time unit(s).

    G(F[0,20](x == 0))

Globally, its always the case that if RampDownInitiated == True holds, then AssistTorque == 0 holds after at most 20 time unit(s).

    G((RampDownInitiated == True) -> F[0,20](AssistTorque == 0))

Globally, its always the case that if RampDownInitiated == True holds, then AssistTorque != 0 holds for at least 19 time unit(s).

    G((RampDownInitiated == True) -> G[0,19](AssistTorque != 0))