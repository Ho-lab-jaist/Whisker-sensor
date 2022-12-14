# Whisker-sensor with tactile compensation ability via adaptive morphology
Data, Data-processing method, Training model for the whisker sensor with damaged structure
![general](https://user-images.githubusercontent.com/74526584/182774621-6ebb8666-3646-4f98-9e90-3b9893c75c93.jpg)
Nature is featured by the resiliency, which enables adaptivity to sudden change under many circumstance. Meanwhile, the resiliency in robotic system is far from comparable to that of the nature. If a robot is partially damaged, often the whole system fails to operate properly. While some approaches have been proposed, the majority of them are focusing on updating the control policy. Such approach, while rather complex, is not always applicable to mechanical damage of the robot body, especially parts that continuously interact with the surrounding environment. In the previous work, we introduced an artificial whiskered sensor that exhibited resilience against physical damage by active change of its morphology around the placement of sensory elements (strain gauges), which allowed compensation of location sensing when the whisker was trimmed. In this paper, we extend the approach by using the whisker sensor for texture discrimination tasks
![whisker_design](https://user-images.githubusercontent.com/74526584/182774788-06fa95d6-019a-49a2-a058-ae8bc6c1143d.jpg)
We demonstrate that changing the morphology of the whisker again helps to reduce mismatching between prior knowledge in the frequency/time domain of the sensory signal. This allows the sensory whisker to recover the tactile perception on texture discrimination after the whisker is partially damaged. Furthermore, we also observe that the using adaptive sensor morphology would augment tactile perception without the need of computationally expensive recognition and re-classification. This work is expected to shed a light on a new generation of robots that automatically work in the open world where self-maintenance against uncertainties is needed.
# Database
Raw data used in this project can be found here: https://drive.google.com/drive/folders/1oKjf4PjfTXIgzhNqt-0lrV5dXCrUjsKF?usp=sharing
# Supportive materials:
1. Paper in Soft Robotics (SORO) journal: https://doi.org/10.1089/soro.2020.0056
2. Paper in IEEE Robotics and Automation Letters (RAL): https://doi.org/10.1109/LRA.2021.3064460
## Notices:
1. In database, data for texture named Knurklebump (KB) is actually Pyramidbump (PB) in the paper
