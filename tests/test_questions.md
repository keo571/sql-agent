# SQL Agent Test Questions

This file contains test questions to validate the SQL agent functionality with the load balancer schema.

## Schema Overview
- **load_balancer**: device_id, device_name, location, vip_id
- **vip**: vip_id, vip_address, port, vip_member_id  
- **vip_member**: member_id, vip_id, member_address, port

## Basic SELECT Queries

1. "Show me all load balancers in us-east"
2. "List all VIP members with port 8080"
3. "What are all the VIP addresses in the system?"
4. "Find load balancers with device names starting with lb-prod"

## Filtering and Conditions

5. "Show me VIPs that use port 443"
6. "List all load balancers that are not in us-west" 
7. "Find VIP members with addresses starting with 192.168"
8. "Show me load balancers in either us-east or us-west"

## JOIN Operations

9. "Show me all load balancers and their VIP addresses"
10. "List all VIP members and their corresponding VIP addresses"
11. "Display load balancer names along with their VIP member addresses"
12. "Show me the complete path from load balancer to VIP member"

## Complex Queries

13. "Show me load balancers in us-east that have VIPs on port 80"
14. "List all VIP members that are associated with load balancers in us-west"
15. "Find load balancers that share the same VIP member"
16. "Show me the distribution of VIP ports across different locations"

## LIKE and Pattern Matching

17. "Find all device names that start with lb-prod"
18. "Show me VIP addresses that end with .1"
19. "List member addresses that contain 168.1"
20. "Find devices with names like LB-PROD%"

## Aggregation and Grouping

21. "How many load balancers are in each location?"
22. "Count the number of VIPs per member"
23. "What's the total number of load balancers per VIP?"
24. "Show me locations with more than 2 load balancers"

## Edge Cases and Error Handling

25. "Are there any load balancers without VIPs?"
26. "Show me VIPs that don't have any members"
27. "List all load balancers that have multiple VIPs"
28. "Find orphaned VIP members"

## Case Insensitivity Tests

29. "Find load balancers in US-EAST"
30. "Show me devices with names like LB-PROD%"
31. "List VIPs with addresses like 10.0.0%"
32. "Find load balancers in Us-EaSt"

## Complex Business Logic

33. "Show me all possible paths from load balancer to member address"
34. "Find load balancers that have VIPs with both port 80 and 443"
35. "List VIP members that are associated with load balancers in us-east and have port 8080"
36. "Show me load balancers and their backup VIP configurations" 