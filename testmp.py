import matplotlib
print(matplotlib.get_backend())
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 1])
plt.title("This is a Test Plot")
print("About to show plot. A window should appear now...")
plt.show()
print("If you see this message, it means the plot window was closed.")