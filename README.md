# 2b2t-Queue-Notifier
A tool to monitor your current position in the 2b2t queue using the latest Minecraft log file and sending updates to a Discord webhook. The estimated time is calculated by taking the first time from the last position and the latest position, finding the difference, and then multiplying that difference by the number of positions left in the queue. However, I wouldn't rely too heavily on this estimate, as times can vary significantly—from 5 minutes between each position (estimating 24 hours) to 10 seconds. While it is likely more accurate than the estimated time provided by the 2b2t server, take that information as you will. It will also notify you if the log file hasn't been updated in 20 seconds (it typically updates every 5 seconds), letting you see if you have been kicked or if your Minecraft has crashed.

# Preview
![image](https://github.com/user-attachments/assets/bc36c4db-a60c-4782-86be-464000e527d4)
![image](https://github.com/user-attachments/assets/40c40b2f-9f0f-4850-94dd-17cb89866397)

# Configuration
You can configure the options in the main Python file. Most settings can remain unchanged; just update the webhook URL and Discord ID to make sure it pings the right account when the queue position hits 1.
