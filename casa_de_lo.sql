BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "clientes" (
	"id_cliente"	TEXT,
	"nome_entidade"	TEXT,
	"tipo_cliente"	TEXT,
	"telemovel"	TEXT,
	"email"	TEXT,
	"id_encomenda_ativa"	TEXT,
	"status_encomenda"	TEXT,
	"valor_total"	REAL,
	"valor_em_divida"	REAL,
	"notas_alergias"	TEXT,
	"password"	TEXT,
	PRIMARY KEY("id_cliente")
);
CREATE TABLE IF NOT EXISTS "encomendas" (
	"id_encomenda"	INTEGER,
	"id_cliente"	TEXT NOT NULL,
	"produtos_texto"	TEXT NOT NULL,
	"valor_total"	REAL NOT NULL,
	"data_pedido"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	"status"	TEXT DEFAULT 'Pendente',
	PRIMARY KEY("id_encomenda" AUTOINCREMENT),
	FOREIGN KEY("id_cliente") REFERENCES "clientes"("id_cliente")
);
INSERT INTO "clientes" VALUES ('CLI001','Maria Antónia Sousa','Particular (B2C)','961234567','m.antonia@email.com','ENC-5','Entregue',70.0,70.0,'Intolerante Lactose / Pão de Ló habitual','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI002','Hotel Douro Charm','Empresa (B2B)','221234567','compras@dourocharm.pt','ENC-6','Em Processamento',480.0,480.0,'Faturação 30 dias / Entrega às 08:30','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI003','Café Central do Porto','Empresa (B2B)','919876543','cafecentral@email.com','ENC-7','Concluída',370.0,0.0,'Sortido de doces conventuais diários','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI004','Mercearia Fina Gaia','Empresa (B2B)','939123456','geral@merccariafina.pt','ENC-8','Agendada (Páscoa)',420.0,420.0,'Sinal pago; Restante contra entrega','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI005','João Pedro Silva','Particular (B2C)','912233445','joao.p@outlook.pt','ENC-9','Pendente Pagamento',55.0,55.0,'Cabaz Especial para oferta','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI006','Gourmet Airport Shop','Empresa (B2B)','229876543','porto@gourmetshop.pt','ENC-10','Em Distribuição',610.0,610.0,'Faturação mensal unificada / Marmeladas','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI007','Ana Maria Sousa ','Particular (B2C)','936903611','ana.m.sousa@gmail.com','ENC-16','Pendente',348.4,348.4,'Vegan','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI008','Dragon Store','Empresa (B2B)','932149667','dragonstore@email.com','ENC-12','Em Distribuição',250.0,250.0,'Leva oferta novo cliente','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI009','Ana Paula Alves','Particular (B2C)','916668606','ana.alves.@email.com','ENC-13','Concluída',125.0,0.0,'Leva oferta novo cliente','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI010','Rita Tavares','Particular (B2C)','936801611','ritinha.tavares@gmail.com','ENC-14','Em Processamento',65.0,65.0,'Entrega noutro endereço','scrypt:32768:8:1$vXyA7M9WkBpQ1zRs$6f8d3a9b2c5e7f1a4ad321b0e9c8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0b9c8d7e6f5a4b3c2d1e0f9a8');
INSERT INTO "clientes" VALUES ('CLI011','Paula Vaz','Particular (B2C)','936902511','paulavazlourenco1970@gmail.com','ENC-26','Pendente',97.4,97.4,'Novo Cliente Oferta','scrypt:32768:8:1$3plQhfvPeGv178Cl$37744c1a7c37b7cca495de65a384f1d9926932f2cc59e7485bc0afacf7ea30dafb15dd2476aa618162b727df6a6a7f84c996bf5f8001f6412a52ebd4a4280fe8');
INSERT INTO "clientes" VALUES ('CLI012','Tontos Por Doces','Empresa (B2B)','935675676','tontospordocesporto@email.com','ENC-19','Pendente',16.0,16.0,'Novo Cliente Oferta','scrypt:32768:8:1$3plQhfvPeGv178Cl$37744c1a7c37b7cca495de65a384f1d9926932f2cc59e7485bc0afacf7ea30dafb15dd2476aa618162b727df6a6a7f84c996bf5f8001f6412a52ebd4a4280fe8');
INSERT INTO "clientes" VALUES ('CLI014','Paulo Bastos','Particular (B2C)','968875645','paulo.bastos@email.com','ENC-18','Pendente',20.2,20.2,'Novo Cliente Oferta','scrypt:32768:8:1$JKhlmnZvoYrkI7wi$0f11d0dc8cd12f1e59198171ca6713659cb151ef6adc8e98d9e7612a7706b8b190f86f1413c0649ace9683168414515b99be66c4a69512de83bac62cd3e431e6');
INSERT INTO "clientes" VALUES ('CLI015','Riba Douro

','Empresa (B2B)','912342345','ribadouro@email.com','ENC-21','Pendente',83.6,83.6,'Novo Cliente Oferta','scrypt:32768:8:1$JKhlmnZvoYrkI7wi$0f11d0dc8cd12f1e59198171ca6713659cb151ef6adc8e98d9e7612a7706b8b190f86f1413c0649ace9683168414515b99be66c4a69512de83bac62cd3e431e6');
INSERT INTO "clientes" VALUES ('CLI016','Lilly Boutique','Empresa (B2B)','913453456','lillyboutiqueporto@gmail.com',NULL,NULL,0.0,0.0,NULL,'scrypt:32768:8:1$JKhlmnZvoYrkI7wi$0f11d0dc8cd12f1e59198171ca6713659cb151ef6adc8e98d9e7612a7706b8b190f86f1413c0649ace9683168414515b99be66c4a69512de83bac62cd3e431e6');
INSERT INTO "clientes" VALUES ('CLI017','Casa da Tia','Empresa (B2B)','921231234','casadatiaporto@gmail.com','ENC-22','Pendente',18.0,18.0,'Novo Cliente Oferta','scrypt:32768:8:1$zfqhulPLKIqGF4Z1$090d67b114eac8e1bb70edf82c7342ef27b342cea2c49d8cb6fa8029a24a0f9e075b1ce4a93154c1f54eb74f2d745c63efa554850ed373fd69adae9801b7aeb7');
INSERT INTO "clientes" VALUES ('CLI018','Rui Pedro Carvalho','Particular (B2C)','912344322','ruicarvalhop@email.com','ENC-20','Pendente',46.0,46.0,'Novo Cliente Oferta','scrypt:32768:8:1$KfBIcl3rFcEctyBe$d28c5d5c5c48084476999ad20bcc75aad818676755e134f0168d84e55ceb15c27653b857920f76c3ac0201e214faf5f511ea6e4818ebb78dfe09a942ef99ecad');
INSERT INTO "clientes" VALUES ('CLI019','Carina de Sousa','Particular (B2C)','923453456','carinasousaprof@email.com','ENC-23','Pendente',46.0,46.0,'Novo Cliente Oferta','scrypt:32768:8:1$KaKbRA0Mrpjj89Ec$33fa31f21684431d6d414d698a703a3c2a1fd611d0a6494d14fd4d44e87130200d8a31dafd6e0fcc568be2fdc09da5933964d5daab7b87c3626d9a2a94112582');
INSERT INTO "clientes" VALUES ('CLI020','Tico Maçarico','Empresa (B2B)','965675675','ticotico@email.com',NULL,NULL,0.0,0.0,NULL,'scrypt:32768:8:1$yatDLndUswx2ZuWD$b99729d89e44b9dec1eddf4a7e523fafbea1b7ce89dee181029745a8f014752008e3fea5defa9f27594f0fb50cec8b858ba4aa340d3a91b29ebce193bddeefe8');
INSERT INTO "clientes" VALUES ('CLI021','Ana Cristina Almeida','Particular (B2C)','932223344','acma2@hotmail.com','ENC-27','Pendente',55.0,55.0,NULL,'scrypt:32768:8:1$F5IDfr3bc7tkdrsB$24fb20a41f4025934933ff261815368bd5b25f4d24c6875c38cac543333b1e5b386c52ebf0971ab583b94e7c7c953eb89345938a9578f03861279ffac1d37196');
INSERT INTO "clientes" VALUES ('CLI022','Cristina Torres','Particular (B2C)','936809611','cristinadastorres@gmail.com','ENC-25','Pendente',136.4,136.4,NULL,'scrypt:32768:8:1$0hruBrr9nT6MlCgs$2739b31f8c76e1f628522e3f36afaeaa5fa915b0a79f898b74b8cbb96b22ffe0aaab8905691f84258b5c9253f30ec392234f28474f8d8cd85bee172976c3d509');
INSERT INTO "encomendas" VALUES (1,'CLI001','Pão de Ló de Margaride, Pastéis de Nata uni.',35.0,'2026-10-21 13:27:53','Entregue');
INSERT INTO "encomendas" VALUES (2,'CLI002','Toucinho do Céu Conventual, Ovos Moles uni.',240.0,'2026-10-21 13:27:53','Em Processamento');
INSERT INTO "encomendas" VALUES (3,'CLI003','Brisas do Lis uni., Arrufadas uni., Folar',185.0,'2026-10-21 13:27:53','Concluída');
INSERT INTO "encomendas" VALUES (4,'CLI011','Folar, Queijadas de Sintra uni., Ovos Moles uni.',9.2,'2026-10-21 13:27:53','Pendente');
INSERT INTO "encomendas" VALUES (5,'CLI001','Pão de Ló de Margaride, Pastéis de Nata uni.',35.0,'2026-10-21 13:29:35','Entregue');
INSERT INTO "encomendas" VALUES (6,'CLI002','Toucinho do Céu Conventual, Ovos Moles (Lote Grande)',240.0,'2026-10-21 13:29:35','Em Processamento');
INSERT INTO "encomendas" VALUES (7,'CLI003','Sortido de doces conventuais diários',185.0,'2026-10-21 13:29:35','Concluída');
INSERT INTO "encomendas" VALUES (8,'CLI004','Folar da Páscoa Especial, Sortido Regional',420.0,'2026-10-21 13:29:35','Agendada (Páscoa)');
INSERT INTO "encomendas" VALUES (9,'CLI005','Cabaz Especial para oferta, Brisas do Lis uni.',55.0,'2026-10-21 13:29:35','Pendente Pagamento');
INSERT INTO "encomendas" VALUES (10,'CLI006','Faturação mensal unificada, Pastelaria Variada',610.0,'2026-10-21 13:29:35','Em Distribuição');
INSERT INTO "encomendas" VALUES (11,'CLI007','Bolo de Mel da Madeira (Sortido Vegan)',310.0,'2026-10-21 13:29:35','Entregue');
INSERT INTO "encomendas" VALUES (12,'CLI008','Leva oferta novo cliente, Queijadas de Sintra',250.0,'2026-10-21 13:29:35','Em Distribuição');
INSERT INTO "encomendas" VALUES (13,'CLI009','Leva oferta novo cliente, Marmelada de Marmelo/Kg',125.0,'2026-10-21 13:29:35','Concluída');
INSERT INTO "encomendas" VALUES (14,'CLI010','Entrega noutro endereço, Compotas/Várias',65.0,'2026-10-21 13:29:35','Em Processamento');
INSERT INTO "encomendas" VALUES (15,'CLI011','Folar, Queijadas de Sintra uni., Ovos Moles uni.',9.2,'2026-10-21 13:29:35','Pendente');
INSERT INTO "encomendas" VALUES (16,'CLI007','Pão de Ló de Margaride, Bolo de Mel da Madeira, Arrufadas uni., Arrufadas uni.',38.4,'2026-10-21 14:03:44','Pendente');
INSERT INTO "encomendas" VALUES (17,'CLI011','Toucinho do Céu Conventual, Toucinho do Céu Conventual',52.0,'2026-10-21 14:11:54','Pendente');
INSERT INTO "encomendas" VALUES (18,'CLI014','Brisas do Lis uni., Brisas do Lis uni., Brisas do Lis uni., Brisas do Lis uni., Marmelada de Marmelo/Kg, Queijadas de Sintra uni., Queijadas de Sintra uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni.',20.2,'2026-10-23 10:13:56','Pendente');
INSERT INTO "encomendas" VALUES (19,'CLI012','Bolo de Mel da Madeira',16.0,'2026-10-26 12:21:15','Pendente');
INSERT INTO "encomendas" VALUES (20,'CLI018','Pão de Ló de Margaride, Toucinho do Céu Conventual',46.0,'2026-10-26 13:13:03','Pendente');
INSERT INTO "encomendas" VALUES (21,'CLI015','Toucinho do Céu Conventual, Toucinho do Céu Conventual, Pão de Ló de Margaride, Marmelada de Marmelo/Kg, Marmelada de Marmelo/Kg',83.6,'2026-10-26 13:20:53','Pendente');
INSERT INTO "encomendas" VALUES (22,'CLI017','Ovos Moles uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni., Ovos Moles uni.',18.0,'2026-10-26 13:27:20','Pendente');
INSERT INTO "encomendas" VALUES (23,'CLI019','Toucinho do Céu Conventual, Pão de Ló de Margaride',46.0,'2026-10-26 13:48:20','Pendente');
INSERT INTO "encomendas" VALUES (24,'CLI011','Pastéis de Nata (Caixa de 6)',9.0,'2026-10-26 14:13:49','Pendente');
INSERT INTO "encomendas" VALUES (25,'CLI022','Toucinho do Céu Conventual, Queijadas de Sintra (Caixa de 6), Ovos Moles (Caixa de 12), Brisas do Lis (Caixa de 6), Arrufadas (Caixa de 6), Pastéis de Nata (Caixa de 6), Pão de Ló de Margaride, Pão de Ló de Margaride, Toucinho do Céu Conventual',136.4,'2026-11-16 15:06:29','Pendente');
INSERT INTO "encomendas" VALUES (26,'CLI011','Pastéis de Nata (Caixa de 6), Pastéis de Nata (Caixa de 6)',18.0,'2026-11-17 09:39:33','Pendente');
INSERT INTO "encomendas" VALUES (27,'CLI021','Toucinho do Céu Conventual, Pão de Ló de Margaride, Pastéis de Nata (Caixa de 6)',55.0,'2026-11-17 14:54:09','Pendente');
CREATE TRIGGER atualizar_cliente_apos_atualizacao
AFTER UPDATE ON encomendas
BEGIN
    UPDATE clientes
    SET 
        id_encomenda_ativa = 'ENC-' || NEW.id_encomenda,
        status_encomenda = NEW.status,
        valor_total = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente),
        valor_em_divida = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente AND status != 'Concluída')
    WHERE id_cliente = NEW.id_cliente;
END;
CREATE TRIGGER atualizar_cliente_apos_insercao
AFTER INSERT ON encomendas
BEGIN
    UPDATE clientes
    SET 
        id_encomenda_ativa = 'ENC-' || NEW.id_encomenda,
        status_encomenda = NEW.status,
        -- Vai à tabela encomendas e soma AUTOMATICAMENTE tudo o que é deste cliente
        valor_total = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente),
        -- Soma AUTOMATICAMENTE o valor em dívida de todas as encomendas não concluídas
        valor_em_divida = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente AND status != 'Concluída')
    WHERE id_cliente = NEW.id_cliente;
END;
COMMIT;

CREATE TRIGGER atualizar_cliente_apos_atualizacao
AFTER UPDATE ON encomendas
BEGIN
    UPDATE clientes
    SET 
        id_encomenda_ativa = 'ENC-' || NEW.id_encomenda,
        status_encomenda = NEW.status,
        valor_total = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente),
        valor_em_divida = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente AND status != 'Concluída')
    WHERE id_cliente = NEW.id_cliente;
END;
CREATE TRIGGER atualizar_cliente_apos_insercao
AFTER INSERT ON encomendas
BEGIN
    UPDATE clientes
    SET 
        id_encomenda_ativa = 'ENC-' || NEW.id_encomenda,
        status_encomenda = NEW.status,
        -- Vai à tabela encomendas e soma AUTOMATICAMENTE tudo o que é deste cliente
        valor_total = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente),
        -- Soma AUTOMATICAMENTE o valor em dívida de todas as encomendas não concluídas
        valor_em_divida = (SELECT COALESCE(SUM(valor_total), 0.0) FROM encomendas WHERE id_cliente = NEW.id_cliente AND status != 'Concluída')
    WHERE id_cliente = NEW.id_cliente;
END;
COMMIT;
