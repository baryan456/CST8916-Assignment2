-- AI assistance: ChatGPT helped write the event-time queries.
SELECT System.Timestamp() AS window_end, deviceType AS device, COUNT(*) AS event_count
INTO traffic
FROM clickstream TIMESTAMP BY [timestamp]
GROUP BY TumblingWindow(second, 10), deviceType;

SELECT System.Timestamp() AS alert_time, COUNT(*) AS click_count
INTO alerts
FROM clickstream TIMESTAMP BY [timestamp]
WHERE event_type = 'product_click'
GROUP BY SlidingWindow(second, 10)
HAVING COUNT(*) >= 3;

SELECT * INTO rawfeed FROM clickstream TIMESTAMP BY [timestamp];
