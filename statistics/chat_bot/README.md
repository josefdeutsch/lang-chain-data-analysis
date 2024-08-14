Here's how you can write Cypher queries using these properties:
1. Calculate the Minimum Low Price:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN min(d.low) AS MinLowPrice
2. Calculate the Maximum High Price:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN max(d.high) AS MaxHighPrice
3. Calculate the Average Closing Price:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN avg(d.close) AS AverageClosePrice
4. Calculate the Total Volume Traded:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN sum(d.volume) AS TotalVolume
5. Calculate the Daily Price Difference (High - Low):
cypher
Copy code
MATCH (d:BTCUSD)
WHERE d.date >= '2024-07-01' AND d.date <= '2024-08-01'
RETURN d.date, (d.high - d.low) AS PriceDifference
ORDER BY d.date
6. Calculate the Percentage Change Between Open and Close:
cypher
Copy code
MATCH (d:BTCUSD)
WHERE d.date >= '2024-07-01' AND d.date <= '2024-08-01'
RETURN d.date, ((d.close - d.open) / d.open) * 100 AS PercentageChange
ORDER BY d.date


7. Calculate the Daily Return (Close to Previous Close): (not working relationship)
cypher
Copy code
MATCH (d1:BTCUSD)-[:NEXT]->(d2:BTCUSD)
RETURN d2.date, ((d2.close - d1.close) / d1.close) * 100 AS DailyReturn

8. Calculate the Median Closing Price:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN percentileCont(d.close, 0.5) AS MedianClosePrice
9. Calculate the Range (High - Low) Over All Data:
cypher
Copy code
MATCH (d:BTCUSD)
WITH max(d.high) AS MaxHigh, min(d.low) AS MinLow
RETURN (MaxHigh - MinLow) AS PriceRange
10. Find the Date with the Highest Trading Volume:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN d.date, d.volume
ORDER BY d.volume DESC
LIMIT 1
11. Calculate the Standard Deviation of Closing Prices:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN stdev(d.close) AS StdDevClosePrice
12. Calculate the Total Number of Trading Days:
cypher
Copy code
MATCH (d:BTCUSD)
RETURN count(d) AS NumberOfTradingDays
13. Calculate the Cumulative Return from Start to End:
cypher
Copy code
MATCH (start:BTCUSD), (end:BTCUSD)
WHERE start.date = '2020-08-08' AND end.date = '2020-08-15'
RETURN ((end.close - start.close) / start.close) * 100 AS CumulativeReturn
14. Find the Day with the Largest Percentage Drop in Closing Price:(not working relationship)cypher
Copy code
MATCH (d1:BTCUSD)-[:NEXT]->(d2:BTCUSD)
WITH d2.date AS Date, ((d2.close - d1.close) / d1.close) * 100 AS PercentChange
RETURN Date, PercentChange
ORDER BY PercentChange ASC
LIMIT 1
15. Calculate the Average Daily Trading Range (High - Low):
cypher
Copy code
MATCH (d:BTCUSD)
RETURN avg(d.high - d.low) AS AverageDailyRange
16. Identify the Days with a Closing Price Higher Than the Opening Price:
cypher
Copy code
MATCH (d:BTCUSD)
WHERE d.date >= '2020-08-08' AND d.date <= '2020-08-15'
AND d.close > d.open
RETURN d.date, d.close, d.open
ORDER BY d.date
17. Calculate the Rolling 7-Day Average Closing Price:
cypher
Copy code
MATCH (d:BTCUSD)
WITH d.date AS Date, d.close AS Close
ORDER BY Date
WITH collect(Close) AS ClosePrices
RETURN apoc.coll.avg(ClosePrices[-7..]) AS Rolling7DayAverage
18. Calculate the Highest Adj Close Price Over a Given Period:
cypher
Copy code
MATCH (d:BTCUSD)
WHERE d.date >= '2020-08-08' AND d.date <= '2020-08-15'
RETURN max(d.adj_close) AS MaxAdjClosePrice
19. Determine the Total Number of Days with Volume Above a Threshold:
cypher
Copy code
MATCH (d:BTCUSD)
WHERE d.volume > 25000000000
RETURN count(d) AS HighVolumeDays
20. Calculate the Volatility as the Standard Deviation of Percentage Changes:(not working relationship)
cypher
Copy code
MATCH (d1:BTCUSD)-[:NEXT]->(d2:BTCUSD)
WITH ((d2.close - d1.close) / d1.close) * 100 AS DailyPercentChange
RETURN stdev(DailyPercentChange) AS Volatility

