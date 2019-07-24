#
# Screen 1
#
u = username
#
# Screen 2
#
u_t = user_type
#
# Screen 3
#
INSERT INTO userr VALUES ('x', 'y','buyer','x@y.com','a','b');
INSERT INTO userr VALUES ('x','1111111111','100','NULL','NULL');
INSERT INTO ADDRESS VALUES ('100','001','street','city','state','11111');
#
#Screen 4
#
INSERT INTO DELIVERER VALUES ('x','y','deliverer','x@y.com','a','b');
#
# Screen 5
#
INSER INTO MANAGER VALUES ('x','y','deliverer','x@y.com','a','b');
# Screen 6 Doesnt do anything
# Screen 7
#
create view screen_7 AS
    SELECT u.first_name, u.lASt_name, u.username, u.email, b.phone, ab.house_number, ab.street, ab.state, ab.city, ab.zip_code, g.store_name, ag.house_number AS g_store_num, ag.street AS g_store_str, p.account_number, p.routing_number
    FROM userr u, buyer b, address ab, grocerystore g, address ag, payments p
    WHERE u.username = b.username AND b.address_id = ab.id AND b.default_store_id = g.store_id AND g.address_id = ag.id AND b.username = p.username AND u.username = 'vitalbetty';

update buyer_info
    set phone = '1011011001'
    WHERE username = 'vitalbetty';
delete FROM userr
    WHERE username = 'vitalbetty';
#
# Screen 8
#
create view screen_8 AS
    SELECT g.store_name, ag.house_number, ag.street, ag.city, ag.state, ag.zip_code, g.phone, g.opening_time, g.closing_time
    FROM grocerystore g, address ag
    WHERE g.address_id = ag.id;
#
# Screen 9 Doesn't do anything
#
# Screen 10
#
fg = food_group
#
# Screen 11
#
create view screen_11 AS
    SELECT i.item_name, i.description, i.listed_price, i.quantity
    FROM item i, soldat s
    WHERE s.store_id = '13' AND i.food_group = 'Beverages';

insert into selectitem values ('1','2','12345')
#
# Screen 12
#
create view screen_12 AS
    SELECT i.item_name, i.description, si.quantity, i.listed_price, i.quantity AS in_store_stock
    FROM orderr o, selectitem si, item i, orderedby ob
    WHERE o.order_id = ob.order_id AND o.order_id = si.order_id AND si.item_id = i.item_id AND o.order_id = '17466' AND ob.buyer_username = 'severelucy';
delete FROM screen_12
    WHERE username = 'severelucy' AND order_id = '17466';
#
# Screen 13
#
create view screen_13 AS
    SELECT *
    FROM orderr o natural join selectitem si natural join item i natural join orderedby ob
    WHERE o.order_id = ob.order_id AND
    o.order_id = si.order_id AND
    si.item_id = i.item_id AND
    o.order_id = '17466';

    SELECT listed_price * quantity
    FROM screen_12;

    SELECT payment_name
    FROM payments natural join buyer
    WHERE buyer.username = 'severelucy';

    update orderr
        set changes
        WHERE order_id = '17466';
#
# Screen 14
#
create view screen_14 AS
    SELECT payment_name, account_number, routing_number, IF(payment_name = default_payment, 'Yes', 'No') AS 'Default' 
    FROM payments natural join buyer
    WHERE buyer.username = 'snobbymorleena';

#
# Screen 15
#

INSERT INTO PAYMENTS VALUES ('vitalbetty','Visa','111111111','111111111');

UPDATE BUYER
SET default_payment='Visa'
WHERE username='vitalbetty';

#
# Screen 16
#
CREATE VIEW screen_16 AS
SELECT O.order_id,O.delivery_time,O.order_placed_time,U.first_name,U.lASt_name,P.payment_name
FROM Orderr O, Payments P, deliveredBy DB, Userr U
WHERE O.order_id=DB.order_id AND DB.deliverer_username=U.username AND O.order_id='17466' AND P.username='vitalbetty' AND p.payment_name='Visa';

SELECT sum(quantity) AS number_of_items
FROM selectitem
WHERE order_id = 17466;


#
#screen 17
CREATE VIEW screen_17 AS
SELECT * FROM 
(
SELECT O.order_id, O.order_placed_date, IF(is_delivered = 1, 'Yes', 'No') AS 'is_delivered', GS.store_name
FROM orderedBy OB, orderr O, deliveredby DB, grocerystore GS, orderFROM OFR
WHERE OB.buyer_username = 'severelucy' AND O.order_id = DB.order_id AND DB.order_id = OB.order_id AND GS.store_id = OFR.store_address_id AND OFR.order_id = OB.order_id
) A
natural join
(
SELECT O.order_id, sum(SI.quantity * I.listed_price) AS 'Total Price', sum(SI.quantity) AS 'Total quantity'
FROM orderr O, selectitem SI, item I, orderedby OB
WHERE O.order_id = SI.order_id AND SI.item_id = I.item_id AND O.order_id = OB.order_id AND OB.buyer_username = 'severelucy'
group by O.order_id
) B
;


# screen 18 nothing

#Screen 19

UPDATE userr
SET email = 'new@new.new'
WHERE username = 'chivalrouspotatoes';

DELETE
FROM userr
WHERE username = 'chivalrouspotatoes'; 

#Screen 20
SELECT *
FROM
(
SELECT GS.store_name AS 'Store Name', O.order_id AS 'Order ID', O.order_placed_date AS 'Date', O.order_placed_time AS 'Time Order Made', O.delivery_time AS 'Time of Delivery'
FROM orderr O, deliveredby DB, grocerystore GS, orderFROM OFR
WHERE DB.deliverer_username = 'chivalrouspotatoes' AND O.order_id = DB.order_id AND GS.store_id = OFR.store_address_id AND OFR.order_id = O.order_id
) A
NATURAL JOIN
(
SELECT O.order_id AS 'Order ID', sum(SI.quantity * I.listed_price) AS 'Order Price', sum(SI.quantity) AS 'Total Number of Items'
FROM orderr O, selectitem SI, item I, deliveredby DB
WHERE O.order_id = SI.order_id AND SI.item_id = I.item_id AND O.order_id = DB.order_id AND DB.deliverer_username = 'chivalrouspotatoes'
group by O.order_id
)B;

#Screen 21

SELECT O.order_placed_time AS 'Order Placed', O.delivery_time AS 'Delivery Time', IF(DB.is_delivered = 1, 'Yes', 'No') AS 'Status', CONCAT(A.house_number, ' ', A.street, ' ', A.city, ', ', A.state,' ', A.zip_code) AS 'Buyer Address', GS.store_name AS 'Store Name'
FROM orderr O, orderFROM OFR, grocerystore GS, address A, orderedby OB, buyer B, deliveredBy DB
WHERE O.order_id = OFR.order_id AND OFR.store_address_id = GS.store_id AND O.order_id = OB.order_id AND OB.buyer_username = B.username AND B.address_id = A.id AND O.order_id = DB.order_id AND O.order_id = 13075;

SELECT I.item_name AS 'item_name', SI.quantity AS 'quantity'
FROM item I, selectitem SI
WHERE I.item_id = SI.item_id AND SI.order_id = 13075;

#Screen 22 nothing

#Screen 23

UPDATE userr 
SET email = 'newemail@email.com'
WHERE username = 'mcdonaldssodium';

#Screen 24 
SELECT sum(SI.quantity) AS 'num_sold', sum(SI.quantity * (I.listed_price - I.wholesale_price)) AS 'profit', sum(SI.quantity * I.listed_price) AS 'revenue', GS.store_name
FROM selectitem SI, item I, grocerystore GS, orderFROM OFR
WHERE SI.item_id = I.item_id AND GS.store_id = OFR.store_address_id AND OFR.order_id = SI.order_id AND OFR.order_id IN (SELECT ofr.order_id 
                                                                                                                        FROM orderFROM ofr, grocerystore gs, manages m 
                                                                                                                        WHERE gs.store_id = ofr.store_address_id AND m.store_address = gs.address_id AND m.username = 'canonxenon');


#Screen 25
SELECT store_name, store_address, order_id, date, total_price, total_items, delivery_address 
FROM(
SELECT o.order_id, gs.store_name, CONCAT(ag.house_number, ' ', ag.street, ' ', ag.city, ', ', ag.state, ' ', ag.zip_code) AS 'store_address', CONCAT(ab.house_number, ' ', ab.street, ' ', ab.city, ', ', ab.state, ' ', ab.zip_code) AS 'delivery_address', O.order_placed_date as 'date' 
FROM orderr o, deliveredby db, orderFROM ofr, grocerystore gs, manages m, address ab, address ag, orderedby ob, buyer b
WHERE db.is_delivered = 0 AND o.order_id = db.order_id AND o.order_id = ofr.order_id AND ofr.store_address_id = gs.store_id AND m.store_address = gs.address_id AND gs.address_id = ag.id AND ob.order_id = o.order_id AND ob.buyer_username = b.username AND ab.id = b.address_id AND m.username = 'lancomegermanium'
) A NATURAL JOIN
(SELECT O.order_id, sum(SI.quantity * I.listed_price) AS 'total_price', sum(SI.quantity) AS 'total_items'
FROM orderr O, selectitem SI, item I
WHERE O.order_id = SI.order_id and SI.item_id = I.item_id 
group by O.order_id) B;


#Screen 26

SELECT I.item_name, I.description, I.quantity, CONCAT('$' , I.listed_price) as 'retail_price', CONCAT('$', I.wholesale_price) as 'wholesale_price', I.exp_date
FROM item I, soldat S
WHERE S.store_id = 2 and I.item_id = S.item_id
GROUP BY I.item_id;

SELECT SUM(I.quantity) as 'total_items'
FROM item I, soldat S 
WHERE S.store_id = 2 and I.item_id = S.item_id;