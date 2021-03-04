DROP TABLE IF EXISTS Orderedproducts;
DROP TABLE IF EXISTS Recommendedproducts;
DROP TABLE IF EXISTS Viewedproducts;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Brands;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Genders;
DROP TABLE IF EXISTS Sessions;
DROP TABLE IF EXISTS Profiles;
DROP TABLE IF EXISTS Sub_categories;
DROP TABLE IF EXISTS Sub_sub_categories;

CREATE TABLE Brands (brandid SERIAL, brand varchar(255), PRIMARY KEY (brandid));
CREATE TABLE Categories (categoryid SERIAL, category varchar(255) NOT NULL, PRIMARY KEY (categoryid));
CREATE TABLE Events (eventid SERIAL, Sessionssessionid varchar(255) NOT NULL, Productsproductid varchar(255), PRIMARY KEY (eventid));
CREATE TABLE Genders (genderid SERIAL, gender varchar(255), PRIMARY KEY (genderid));
CREATE TABLE Orderedproducts (orderedproductid SERIAL, Sessionssessionid varchar(255) NOT NULL, Productsproductid varchar(255) NOT NULL, PRIMARY KEY (orderedproductid));
CREATE TABLE Products (productid varchar(255) NOT NULL, name varchar(255), description varchar(1023), price float, herhaalaankopen BIT, recommendable BIT, Profilesprofileid varchar(255), Brandsbrandid int, Categoriescategoryid int, Sub_sub_categoriessub_sub_categoryid int, Sub_categoriessub_categoryid int, Gendersgenderid int, PRIMARY KEY (productid));
CREATE TABLE Profiles (profileid varchar(255) NOT NULL, PRIMARY KEY (profileid));
CREATE TABLE Recommendedproducts (recommendedproductid SERIAL, Profilesprofileid varchar(255) NOT NULL, Productsproductid varchar(255) NOT NULL, PRIMARY KEY (recommendedproductid));
CREATE TABLE Sessions (sessionid varchar(255) NOT NULL, Profilesprofileid varchar(255) NOT NULL, sessionstart timestamp NOT NULL, sessionend timestamp NOT NULL, has_sale BIT NOT NULL, PRIMARY KEY (sessionid));
CREATE TABLE Sub_categories (sub_categoryid SERIAL, sub_category varchar(255) NOT NULL, PRIMARY KEY (sub_categoryid));
CREATE TABLE Sub_sub_categories (sub_sub_categoryid SERIAL, sub_sub_category varchar(255) NOT NULL, PRIMARY KEY (sub_sub_categoryid));
CREATE TABLE Viewedproducts (viewedproductid SERIAL, Profilesprofileid varchar(255) NOT NULL, Productsproductid varchar(255) NOT NULL, PRIMARY KEY (viewedproductid));
ALTER TABLE Viewedproducts ADD CONSTRAINT FKViewedprod516306 FOREIGN KEY (Productsproductid) REFERENCES Products (productid);
ALTER TABLE Viewedproducts ADD CONSTRAINT FKViewedprod836821 FOREIGN KEY (Profilesprofileid) REFERENCES Profiles (profileid);
ALTER TABLE Recommendedproducts ADD CONSTRAINT FKRecommende637348 FOREIGN KEY (Productsproductid) REFERENCES Products (productid);
ALTER TABLE Recommendedproducts ADD CONSTRAINT FKRecommende316833 FOREIGN KEY (Profilesprofileid) REFERENCES Profiles (profileid);
ALTER TABLE Products ADD CONSTRAINT FKProducts505288 FOREIGN KEY (Gendersgenderid) REFERENCES Genders (genderid);
ALTER TABLE Products ADD CONSTRAINT FKProducts973090 FOREIGN KEY (Sub_categoriessub_categoryid) REFERENCES Sub_categories (sub_categoryid);
ALTER TABLE Products ADD CONSTRAINT FKProducts978174 FOREIGN KEY (Sub_sub_categoriessub_sub_categoryid) REFERENCES Sub_sub_categories (sub_sub_categoryid);
ALTER TABLE Sessions ADD CONSTRAINT FKSessions493177 FOREIGN KEY (Profilesprofileid) REFERENCES Profiles (profileid);
ALTER TABLE Events ADD CONSTRAINT FKEvents31703 FOREIGN KEY (Productsproductid) REFERENCES Products (productid);
ALTER TABLE Events ADD CONSTRAINT FKEvents467990 FOREIGN KEY (Sessionssessionid) REFERENCES Sessions (sessionid);
ALTER TABLE Orderedproducts ADD CONSTRAINT FKOrderedpro121984 FOREIGN KEY (Productsproductid) REFERENCES Products (productid);
ALTER TABLE Orderedproducts ADD CONSTRAINT FKOrderedpro685696 FOREIGN KEY (Sessionssessionid) REFERENCES Sessions (sessionid);
ALTER TABLE Products ADD CONSTRAINT FKProducts897994 FOREIGN KEY (Categoriescategoryid) REFERENCES Categories (categoryid);
ALTER TABLE Products ADD CONSTRAINT FKProducts577926 FOREIGN KEY (Brandsbrandid) REFERENCES Brands (brandid);
ALTER TABLE Products ADD CONSTRAINT FKProducts634987 FOREIGN KEY (Profilesprofileid) REFERENCES Profiles (profileid);