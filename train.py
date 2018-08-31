import aiml
import os

k = aiml.Kernel()
k.bootstrap(learnFiles="std-startup.aiml", commands="load aiml b")
k.saveBrain("brain.dump")
print("Training complete!")