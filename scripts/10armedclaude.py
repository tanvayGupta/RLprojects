import numpy as np
import matplotlib.pyplot as plt
import os

np.random.seed(67)

LOG_FILE = "bandit_logs.npz"


def armRNG(arms=10):
    # row 0: true means (0 to 1), row 1: standard deviations (0.1 to 0.2)
    x = np.array([np.round(np.random.rand(arms), 3),
                  0.1 + np.round((np.random.rand(arms)) / 10, 3)])
    return x


def RLagent(hiddenRewards, epsilon=0.1, iterations=1000):
    arms = hiddenRewards.shape[1]
    trueMeans = hiddenRewards[0]
    bestArm = np.argmax(trueMeans)       # used ONLY for logging, never for decisions

    rewardArray = np.zeros(arms)         # the agent's Q estimates
    iterationArray = np.ones(arms)

    # --- logs ---
    rewards = np.zeros(iterations)       # reward received at each step
    optimal = np.zeros(iterations)       # 1 if the best arm was chosen
    qError = np.zeros(iterations)        # mean |Q - true mean| across arms

    for i in range(iterations):
        r = np.random.rand()
        if r <= epsilon:                                   # exploration
            rIndex = np.random.randint(0, arms)
        else:                                              # exploitation
            rIndex = np.argmax(rewardArray)

        reward = np.clip(np.round(np.random.normal(
            loc=hiddenRewards[0][rIndex], scale=hiddenRewards[1][rIndex]), 3), -1, 1)

        rewardArray[rIndex] += (reward - rewardArray[rIndex]) / iterationArray[rIndex]
        iterationArray[rIndex] += 1

        rewards[i] = reward
        optimal[i] = (rIndex == bestArm)
        qError[i] = np.mean(np.abs(rewardArray - trueMeans))

    return rewards, optimal, qError, rewardArray.copy()


def run_experiments(epsilons, runs=200, arms=10, iterations=1000):
    E = len(epsilons)
    data = {
        "epsilons": np.array(epsilons),
        "reward":   np.zeros((E, runs, iterations)),
        "optimal":  np.zeros((E, runs, iterations)),
        "qerr":     np.zeros((E, runs, iterations)),
        "finalQ":   np.zeros((E, runs, arms)),
        "trueMeans": np.zeros((runs, arms)),
    }
    for run in range(runs):
        hidden = armRNG(arms)                 # one environment per run...
        data["trueMeans"][run] = hidden[0]
        for e, eps in enumerate(epsilons):    # ...shared by every epsilon
            rew, opt, err, q = RLagent(hidden, eps, iterations)
            data["reward"][e, run] = rew
            data["optimal"][e, run] = opt
            data["qerr"][e, run] = err
            data["finalQ"][e, run] = q
    return data


def plot_results(data, save_as="bandit_results.png"):
    eps = data["epsilons"]
    fig, axes = plt.subplots(2, 2, figsize=(13, 9))
    colors = plt.cm.viridis(np.linspace(0, 0.9, len(eps)))

    for e, eps_val in enumerate(eps):
        label, c = f"ε = {eps_val}", colors[e]
        axes[0, 0].plot(data["reward"][e].mean(axis=0), label=label, color=c)
        axes[0, 1].plot(data["optimal"][e].mean(axis=0) * 100, label=label, color=c)
        axes[1, 0].plot(data["qerr"][e].mean(axis=0), label=label, color=c)
        axes[1, 1].scatter(data["trueMeans"].ravel(), data["finalQ"][e].ravel(),
                           s=8, alpha=0.25, label=label, color=c)

    axes[0, 0].set(title="Average reward per step", xlabel="Step", ylabel="Reward")
    axes[0, 1].set(title="% optimal action", xlabel="Step", ylabel="%")
    axes[1, 0].set(title="Estimation error (mean |Q − true mean|)", xlabel="Step", ylabel="Error")
    axes[1, 1].plot([0, 1], [0, 1], "k--", lw=1, label="perfect estimate")
    axes[1, 1].set(title="Final Q vs true mean (all runs, all arms)",
                   xlabel="True mean", ylabel="Estimated Q")

    for ax in axes.ravel():
        ax.grid(alpha=0.3)
        ax.legend()

    plt.tight_layout()
    plt.savefig(save_as, dpi=150)
    plt.show()


if __name__ == "__main__":
    RERUN = True          # set False to re-plot saved logs without re-simulating
    epsilons = [0, 0.01, 0.1]

    if RERUN or not os.path.exists(LOG_FILE):
        data = run_experiments(epsilons, runs=200, arms=10, iterations=1000)
        np.savez(LOG_FILE, **data)
        print(f"Logs saved to {LOG_FILE}")
    else:
        data = dict(np.load(LOG_FILE))
        print(f"Loaded logs from {LOG_FILE}")

    plot_results(data)