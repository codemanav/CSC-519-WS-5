import time
import requests
import matplotlib.pyplot as plt

URL = f"http://152.7.177.200/"

def benchmark():
    times = []
    for i in range(30):
        start = time.time()
        r = requests.get(URL)
        end = time.time()
        times.append((end - start) * 1000)
    return times

def main():
    print("Running benchmark for Config 1 (Single VM)...")
    input("➡️ Make sure Config 1 is deployed (press Enter when ready)")
    times1 = benchmark()

    print("Running benchmark for Config 2 (Two VMs)...")
    input("➡️ Make sure Config 2 is deployed (press Enter when ready)")
    times2 = benchmark()

    # Plot side-by-side histograms
    plt.figure(figsize=(10, 5))

    plt.hist(times1, bins=10, alpha=0.7, label="Config 1 (Single VM)", color="blue", edgecolor="black")
    plt.hist(times2, bins=10, alpha=0.7, label="Config 2 (Two VMs)", color="orange", edgecolor="black")

    plt.title("Response Times Comparison: Config 1 vs Config 2")
    plt.xlabel("Response Time (ms)")
    plt.ylabel("Frequency")
    plt.legend()

    plt.savefig("config_comparison_histogram.png")
    plt.show()

    print("\n✅ Saved as config_comparison_histogram.png")

if __name__ == "__main__":
    main()
