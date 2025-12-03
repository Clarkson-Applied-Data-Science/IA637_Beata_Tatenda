--------1. Daily Appointment Count (How busy is the clinic?)
SELECT 
    date AS day,
    COUNT(*) AS total
FROM appointment
GROUP BY date
ORDER BY date;


--------2. Doctor Appointment Volume (Last 30 Days)
SELECT
    u.name AS doctor_name,
    COUNT(a.aid) AS total
FROM appointment a
JOIN user u ON a.doctorid = u.uid
WHERE a.date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY a.doctorid
ORDER BY total DESC;

---------3.Appointment Check-In Conversion Rate
SELECT 
    (SELECT COUNT(*) FROM checkin) /
    (SELECT COUNT(*) FROM appointment) AS rate;


---------4. Most Common Appointment Times (Hourly Distribution)
SELECT 
    HOUR(STR_TO_DATE(time, '%H:%i')) AS hour,
    COUNT(*) AS total
FROM appointment
GROUP BY hour
ORDER BY hour;

