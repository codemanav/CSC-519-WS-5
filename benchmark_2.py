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

    # Create box-and-whisker plot
    plt.figure(figsize=(8, 6))
    plt.boxplot([times2, times1], labels=["Config 1 (Single VM)", "Config 2 (Two VMs)"])

    plt.title("Response Times Comparison (Box-and-Whisker)")
    plt.ylabel("Response Time (ms)")

    plt.savefig("config_comparison_boxplot.png")
    plt.show()

    print("\n✅ Saved as config_comparison_boxplot.png")

if __name__ == "__main__":
    main()
