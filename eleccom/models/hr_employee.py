import re
from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    name = fields.Char(string='Nombre Completo', compute='_compute_name', store=True, readonly=False)
    rut = fields.Char(string='RUT')
    centro_costo_Codigo = fields.Integer(string='Centro de Costo Codigo')
    centro_costo_nombre = fields.Char(string='Centro de Costo Nombre')
    nombre = fields.Char(string='Nombres')
    apellido_paterno = fields.Char(string='Apellido Paterno')
    apellido_materno = fields.Char(string='Apellido Materno')
    nombre_completo = fields.Char(
        string='Nombre Completo', 
        compute='_compute_nombre_completo', 
        store=True)
    
    direccion = fields.Char(string='Dirección')
    comuna = fields.Char(string='Comuna')
    telefono_personal = fields.Char(string='Teléfono Personal')
    email_personal = fields.Char(string='Email Personal')

    fecha_nacimiento = fields.Date(string='Fecha de Nacimiento')
    chileno = fields.Selection([
        ('S', 'SI'),
        ('N', 'NO')
    ], string='Chileno', default='S')
    nacionalidad = fields.Char(string='Nacionalidad')
    sexo = fields.Selection([
        ('M', 'Masculino'),
        ('F', 'Femenino')
    ], string='Sexo')
    celular = fields.Char(string='Celular')
    cargo = fields.Char(string='Cargo')
    
    sueldo = fields.Float(string='Sueldo Mensual')
    sueldo_uf = fields.Float(string='Sueldo Mensual en UF')
    sueldo_diario = fields.Float(string='Sueldo Diario')
    sueldo_hora = fields.Float(string='Sueldo por Hora')
    sueldo_empresarial = fields.Selection([
        ('S', 'SI'),
        ('N', 'NO')
    ], string='Sueldo Empresarial', default='N')
    
    isapre = fields.Selection([
        ('BANM', 'Banmedica'),
        ('BEST', 'BANCO ESTADO'),
        ('CMN', 'Colmena'),
        ('cons', 'Consalud'),
        ('CRZB', 'CRUZ BLANCA'),
        ('ESE', 'ESENCIAL'),
        ('fona', 'Fonasa'),
        ('ISAL', 'ISAPRE ISALUD'),
        ('MAS2', 'NUEVA MASVIDA'),
        ('masv', 'NO VIGENTE Mas Vida'),
        ('SIN', 'SIN ISAPRE'),
        ('VID3', 'VIDA TRES')
    ], string='Isapre')
    
    fun_isapre = fields.Char(string='FUN Isapre')
    cotizacion_pactada_salud = fields.Float(string='Cotización Salud UF')
    cotizacion_pactada_salud_pesos = fields.Float(string='Cotización Salud Pesos')
    cotizacion_pactada_salud_porcentaje = fields.Float(string='% Salud Colectivo')
    
    afp = fields.Selection([
        ('CUMP', 'Cuprum'),
        ('EMPA', 'Empart.'),
        ('HABI', 'Habitat'),
        ('MODE', 'Modelo'),
        ('PROV', 'Provida'),
        ('PVIT', 'Plan Vital'),
        ('SIN', 'SIN AFP'),
        ('SSS', 'Servicio Seguro social'),
        ('STMA', 'Capital'),
        ('UNO', 'UNO')
    ], string='AFP')
    
    tipo_trabajador = fields.Selection([
        ('0', '0- Activo'),
        ('1', '1- Pensionado y Cot.'),
        ('2', '2- Pensionado no Cot.'),
        ('3', '3- Activo > 65 años')
    ], string='Tipo Trabajador')
    
    monto_cuenta2_afp = fields.Float(string='Cuenta 2 AFP')
    seguro_cesantia = fields.Float(string='Seguro de Cesantía Trabajador')
    seguro_cesantia_empleador = fields.Float(string='Seguro de Cesantía Empleador')
    numero_cargas_familiares = fields.Integer(string='Número de Cargas')
    
    ahorro_voluntario = fields.Float(string='APV')
    apv_uf = fields.Float(string='APV UF')
    empresa_apv = fields.Selection([
        ('000', 'No Cotiza A.P.V.'),
        ('003', 'Cuprum'),
        ('005', 'Habitat'),
        ('008', 'Provida'),
        ('029', 'Planvital'),
        ('033', 'Capital'),
        ('034', 'Modelo'),
        ('073', 'CAJA DE COMPENSACION LOS ANDES'),
        ('100', 'ABN AMRO (CHILE) SEGUROS DE VIDA S.A.'),
        ('101', 'AGF ALLIANZ CHILE COMPAÑIA DE SEGUROS VIDA S.A'),
        ('102', 'SANTANDER SEGUROS DE VIDA S.A.'),
        ('103', 'BCI SEGUROS VIDA S.A.'),
        ('104', 'BANCHILE SEGUROS DE VIDA S.A.'),
        ('105', 'BBVA SEGUROS DE VIDA S.A.'),
        ('106', 'BICE VIDA COMPAÑIA DE SEGUROS S.A.'),
        ('107', 'Zurich Chile Seguros de Vida'),
        ('108', 'CIGNA COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('109', 'CN LIFE, COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('110', 'COMPAÑIA DE SEGUROS DE VIDA CARDIF S.A.'),
        ('111', 'CIA DE SEG. DE VIDA CONSORCIO NACIONAL DE SEG S.A.'),
        ('118', 'SEGUROS DE VIDA SURA S.A.'),
        ('121', 'METLIFE CHILE SEGUROS DE VIDA S.A.'),
        ('123', 'MAPFRE COMPAÑIA DE SEGUROS DE VIDA DE CHILE S.A.'),
        ('125', 'MUTUAL DE SEGUROS DE CHILE'),
        ('126', 'MUTUALIDAD DE CARabINEROS'),
        ('127', 'MUTUALIDAD DEL EJERCITO Y AVIACION'),
        ('128', 'OHIO NATIONAL SEGUROS DE VIDA S.A.'),
        ('129', 'PRINCIPAL COMPAÑIA DE SEGUROS DE VIDA CHILE S.A.'),
        ('130', 'RENTA NACIONAL COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('131', 'SEGUROS DE VIDA SECURITY PREVISION S.A.'),
        ('134', 'COMPAÑIA DE SEGUROS GENERALES PENTA-SECURITY S.A.'),
        ('135', 'PENTA VIDA COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('136', 'ACE SEGUROS S.A.'),
        ('201', 'BANDESARROLLO ADM. GENERAL DE FONDOS S.A.'),
        ('204', 'BCI ASSET MANAGEMENT ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('205', 'BICE INVERSIONES AGF S.A.'),
        ('208', 'BTG PACTUAL CHILE S.A. ADMINISTRADORA GENERAL DE FONDOS'),
        ('210', 'CORPBANCA ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('213', 'LARRAIN VIAL S.A. CORREDORA DE BOLSA'),
        ('214', 'PRINCIPAL ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('215', 'SANTANDER ASSET MANAGEMENT S.A. ADM. GENERAL DE FONDOS'),
        ('217', 'SCOTIA SUD AMERICANO ADMINISTRADORA DE FONDOS MUTUOS S.A.'),
        ('218', 'ADMINISTRADORA GENERAL DE FONDOS SECURITY S.A.'),
        ('219', 'CRUZ DEL SUR CORREDORA DE BOLSA S.A.'),
        ('222', 'BANCHILE CORREDORES DE BOLSA S.A.'),
        ('225', 'ITAU ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('227', 'CORREDORES DE BOLSA SURA S.A.'),
        ('228', 'BTG PACTUAL CHILE S.A. CORREDORES DE BOLSA'),
        ('229', 'BANCOESTADO S.A. ADMINISTRADORA GENERAL DE FONDOS'),
        ('231', 'SCOTIA SUD AMERICANO CORREDORES DE BOLSA S.A.'),
        ('232', 'BICE INVERSIONES CORREDORES DE BOLSA S.A.'),
        ('303', 'BBVA Banco Bhif'),
        ('319', 'Banco Ripley'),
        ('320', 'Banco ScotiaBank'),
        ('321', 'Banco Santander Santiago'),
        ('400', 'CAJA DE COMPENSACION LOS ANDES'),
        ('600', 'ZURICH CHILE ASSET MANAGEMENT ADMINISTRADORA GENERAL DE FONDOS S.A'),
        ('601', 'Larrain Vial Admin. General de fondos S.A.')
    ], string='Empresa APV')
    
    forma_pago_apv = fields.Selection([
        ('1', '1.- Directa a la institución'),
        ('2', '2.- Directa a la institución')
    ], string='Forma de Pago APV')
    
    apv_reg = fields.Selection([
        ('A', 'A'),
        ('B', 'B')
    ], string='Reg. Letra APV')
    
    tipo_impuesto = fields.Selection([
        ('1', 'Impuesto de Segunda Categoría'),
        ('2', 'Impuesto Único Obrero Agrícola'),
        ('3', 'Impuesto Adicional')
    ], string='Tipo de Impuesto')
    
    trabajador_agricola = fields.Selection([
        ('S', 'SI'),
        ('N', 'NO')
    ], string='Trabajador Agrícola', default='N')
    
    prestamo_solidario = fields.Selection([
        ('S', 'SI'),
        ('N', 'NO')
    ], string='Préstamo Solidario', default='N')
    
    ahorro_voluntario2 = fields.Float(string='APV2')
    apv_uf2 = fields.Float(string='APV2 UF')
    empresa_apv2 = fields.Selection([
        ('000', 'No Cotiza A.P.V.'),
        ('003', 'Cuprum'),
        ('005', 'Habitat'),
        ('008', 'Provida'),
        ('029', 'Planvital'),
        ('033', 'Capital'),
        ('034', 'Modelo'),
        ('073', 'CAJA DE COMPENSACION LOS ANDES'),
        ('100', 'ABN AMRO (CHILE) SEGUROS DE VIDA S.A.'),
        ('101', 'AGF ALLIANZ CHILE COMPAÑIA DE SEGUROS VIDA S.A'),
        ('102', 'SANTANDER SEGUROS DE VIDA S.A.'),
        ('103', 'BCI SEGUROS VIDA S.A.'),
        ('104', 'BANCHILE SEGUROS DE VIDA S.A.'),
        ('105', 'BBVA SEGUROS DE VIDA S.A.'),
        ('106', 'BICE VIDA COMPAÑIA DE SEGUROS S.A.'),
        ('107', 'Zurich Chile Seguros de Vida'),
        ('108', 'CIGNA COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('109', 'CN LIFE, COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('110', 'COMPAÑIA DE SEGUROS DE VIDA CARDIF S.A.'),
        ('111', 'CIA DE SEG. DE VIDA CONSORCIO NACIONAL DE SEG S.A.'),
        ('118', 'SEGUROS DE VIDA SURA S.A.'),
        ('121', 'METLIFE CHILE SEGUROS DE VIDA S.A.'),
        ('123', 'MAPFRE COMPAÑIA DE SEGUROS DE VIDA DE CHILE S.A.'),
        ('125', 'MUTUAL DE SEGUROS DE CHILE'),
        ('126', 'MUTUALIDAD DE CARabINEROS'),
        ('127', 'MUTUALIDAD DEL EJERCITO Y AVIACION'),
        ('128', 'OHIO NATIONAL SEGUROS DE VIDA S.A.'),
        ('129', 'PRINCIPAL COMPAÑIA DE SEGUROS DE VIDA CHILE S.A.'),
        ('130', 'RENTA NACIONAL COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('131', 'SEGUROS DE VIDA SECURITY PREVISION S.A.'),
        ('134', 'COMPAÑIA DE SEGUROS GENERALES PENTA-SECURITY S.A.'),
        ('135', 'PENTA VIDA COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('136', 'ACE SEGUROS S.A.'),
        ('201', 'BANDESARROLLO ADM. GENERAL DE FONDOS S.A.'),
        ('204', 'BCI ASSET MANAGEMENT ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('205', 'BICE INVERSIONES AGF S.A.'),
        ('208', 'BTG PACTUAL CHILE S.A. ADMINISTRADORA GENERAL DE FONDOS'),
        ('210', 'CORPBANCA ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('213', 'LARRAIN VIAL S.A. CORREDORA DE BOLSA'),
        ('214', 'PRINCIPAL ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('215', 'SANTANDER ASSET MANAGEMENT S.A. ADM. GENERAL DE FONDOS'),
        ('217', 'SCOTIA SUD AMERICANO ADMINISTRADORA DE FONDOS MUTUOS S.A.'),
        ('218', 'ADMINISTRADORA GENERAL DE FONDOS SECURITY S.A.'),
        ('219', 'CRUZ DEL SUR CORREDORA DE BOLSA S.A.'),
        ('222', 'BANCHILE CORREDORES DE BOLSA S.A.'),
        ('225', 'ITAU ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('227', 'CORREDORES DE BOLSA SURA S.A.'),
        ('228', 'BTG PACTUAL CHILE S.A. CORREDORES DE BOLSA'),
        ('229', 'BANCOESTADO S.A. ADMINISTRADORA GENERAL DE FONDOS'),
        ('231', 'SCOTIA S Sud AMERICANO CORREDORES DE BOLSA S.A.'),
        ('232', 'BICE INVERSIONES CORREDORES DE BOLSA S.A.'),
        ('303', 'BBVA Banco Bhif'),
        ('319', 'Banco Ripley'),
        ('320', 'Banco ScotiaBank'),
        ('321', 'Banco Santander Santiago'),
        ('400', 'CAJA DE COMPENSACION LOS ANDES'),
        ('600', 'ZURICH CHILE ASSET MANAGEMENT ADMINISTRADORA GENERAL DE FONDOS S.A'),
        ('601', 'Larrain Vial Admin. General de fondos S.A.')
    ], string='Empresa APV2')
    
    forma_pago_apv2 = fields.Selection([
        ('1', '1.- Directa a la institución'),
        ('2', '2.- Directa to the institución')
    ], string='Forma de Pago APV2')
    
    apv_reg2 = fields.Selection([
        ('A', 'A'),
        ('B', 'B')
    ], string='Reg. Letra APV2')
    
    empresa_apvc = fields.Selection([
        ('000', 'No Cotiza A.P.V.'),
        ('003', 'Cuprum'),
        ('005', 'Habitat'),
        ('008', 'Provida'),
        ('029', 'Planvital'),
        ('033', 'Capital'),
        ('034', 'Modelo'),
        ('073', 'CAJA DE COMPENSACION LOS ANDES'),
        ('100', 'ABN AMRO (CHILE) SEGUROS DE VIDA S.A.'),
        ('101', 'AGF ALLIANZ CHILE COMPAÑIA DE SEGUROS VIDA S.A'),
        ('102', 'SANTANDER SEGUROS DE VIDA S.A.'),
        ('103', 'BCI SEGUROS VIDA S.A.'),
        ('104', 'BANCHILE SEGUROS DE VIDA S.A.'),
        ('105', 'BBVA SEGUROS DE VIDA S.A.'),
        ('106', 'BICE VIDA COMPAÑIA DE SEGUROS S.A.'),
        ('107', 'Zurich Chile Seguros de Vida'),
        ('108', 'CIGNA COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('109', 'CN LIFE, COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('110', 'COMPAÑIA DE SEGUROS DE VIDA CARDIF S.A.'),
        ('111', 'CIA DE SEG. DE VIDA CONSORCIO NACIONAL DE SEG S.A.'),
        ('118', 'SEGUROS DE VIDA SURA S.A.'),
        ('121', 'METLIFE CHILE SEGUROS DE VIDA S.A.'),
        ('123', 'MAPFRE COMPAÑIA DE SEGUROS DE VIDA DE CHILE S.A.'),
        ('125', 'MUTUAL DE SEGUROS DE CHILE'),
        ('126', 'MUTUALIDAD DE CARabINEROS'),
        ('127', 'MUTUALIDAD DEL EJERCITO Y AVIACION'),
        ('128', 'OHIO NATIONAL SEGUROS DE VIDA S.A.'),
        ('129', 'PRINCIPAL COMPAÑIA DE SEGUROS DE VIDA CHILE S.A.'),
        ('130', 'RENTA NACIONAL COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('131', 'SEGUROS DE VIDA SECURITY PREVISION S.A.'),
        ('134', 'COMPAÑIA DE SEGUROS GENERALES PENTA-SECURITY S.A.'),
        ('135', 'PENTA VIDA COMPAÑIA DE SEGUROS DE VIDA S.A.'),
        ('136', 'ACE SEGUROS S.A.'),
        ('201', 'BANDESARROLLO ADM. GENERAL DE FONDOS S.A.'),
        ('204', 'BCI ASSET MANAGEMENT ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('205', 'BICE INVERSIONES AGF S.A.'),
        ('208', 'BTG PACTUAL CHILE S.A. ADMINISTRADORA GENERAL DE FONDOS'),
        ('210', 'CORPBANCA ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('213', 'LARRAIN VIAL S.A. CORREDORA DE BOLSA'),
        ('214', 'PRINCIPAL ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('215', 'SANTANDER ASSET MANAGEMENT S.A. ADM. GENERAL DE FONDOS'),
        ('217', 'SCOTIA SUD AMERICANO ADMINISTRADORA DE FONDOS MUTUOS S.A.'),
        ('218', 'ADMINISTRADORA GENERAL DE FONDOS SECURITY S.A.'),
        ('219', 'CRUZ DEL SUR CORREDORA DE BOLSA S.A.'),
        ('222', 'BANCHILE CORREDORES DE BOLSA S.A.'),
        ('225', 'ITAU ADMINISTRADORA GENERAL DE FONDOS S.A.'),
        ('227', 'CORREDORES DE BOLSA SURA S.A.'),
        ('228', 'BTG PACTUAL CHILE S.A. CORREDORES DE BOLSA'),
        ('229', 'BANCOESTADO S.A. ADMINISTRADORA GENERAL DE FONDOS'),
        ('231', 'SCOTIA SUD AMERICANO CORREDORES DE BOLSA S.A.'),
        ('232', 'BICE INVERSIONES CORREDORES DE BOLSA S.A.'),
        ('303', 'BBVA Banco Bhif'),
        ('319', 'Banco Ripley'),
        ('320', 'Banco ScotiaBank'),
        ('321', 'Banco Santander Santiago'),
        ('400', 'CAJA DE COMPENSACION LOS ANDES'),
        ('600', 'ZURICH CHILE ASSET MANAGEMENT ADMINISTRADORA GENERAL DE FONDOS S.A'),
        ('601', 'Larrain Vial Admin. General de fondos S.A.')
    ], string='Empresa APV Colectivo')
    
    ahorro_voluntarioc = fields.Float(string='APV Colectivo')
    forma_pago_apvc = fields.Selection([
        ('1', '1.- Directa a la institución'),
        ('2', '2.- Directa to the institución')
    ], string='Forma de Pago APVC')
    
    apv_regc = fields.Selection([
        ('A', 'A'),
        ('B', 'B')
    ], string='Reg. Letra APVC')
    
    apv_ufc = fields.Float(string='APV UF Colectivo')
    porcentaje_apvc_trab = fields.Float(string='% Trabajador APVC')
    
    prestamo_caja = fields.Float(string='Préstamo Caja')
    prestamo_caja2 = fields.Float(string='Préstamo 2da Caja')
    caja = fields.Selection([
        ('00', 'Sin CCAF'),
        ('01', 'Los Andes'),
        ('02', 'La Araucana'),
        ('03', 'Los Héroes'),
        ('05', 'Gabriela Mistral'),
        ('06', '18 de Septiembre')
    ], string='2nda Caja de Compensación')
    
    caja_trabajador = fields.Selection([
        ('00', 'Sin CCAF'),
        ('01', 'Los Andes'),
        ('02', 'La Araucana'),
        ('03', 'Los Héroes'),
        ('05', 'Gabriela Mistral'),
        ('06', '18 de Septiembre')
    ], string='Caja de Compensación Trabajador')
    
    seguro_accidente = fields.Selection([
        ('1', 'SI'),
        ('0', 'NO')
    ], string='Seguro de Accidente', default='1')
    
    fecha_primera_afiliacion = fields.Date(string='Fecha de Primera Afiliación')
    
    afiliado_voluntario = fields.Boolean(string='Afiliado Voluntario', default=False)

    fecha_contrato = fields.Date(string="Fecha Contrato")
    fecha_termino_contrato = fields.Date(string="Fecha Término Contrato")
    fecha_contrato = fields.Date(string="Fecha de Ingreso")

    clausula_termino = fields.Selection([
        ('3', 'Art. 159 N°1: Mutuo acuerdo de las partes'),
        ('4', 'Art. 159 N°2: Renuncia Del Trabajador'),
        ('5', 'Art. 159 N°3: Muerte del trabajador'),
        ('6', 'Art. 159 N°4: Vencimiento del plazo convenido'),
        ('7', 'Art. 159 N°5: Conclusión del trabajo o servicio'),
        ('8', 'Art. 159 N°6: Caso fortuito o fuerza mayor'),
        ('11', 'Art. 160 N° 2: Negociaciones prohibidas por escrito'),
        ('12', 'Art. 160 N° 3: No concurrencia a las labores'),
        ('13', 'Art. 160 N° 4: Abandono del trabajo'),
        ('14', 'Art. 160 N° 5: Actos, omisiones o imprudencias temerarias'),
        ('15', 'Art. 160 N° 6: Perjuicio material causado intencionalmente'),
        ('16', 'Art. 160 N° 7: Incumplimiento grave de las obligaciones'),
        ('18', 'Art. 161 Inciso 1°: Necesidades de la empresa'),
        ('19', 'Art. 161 Inciso 2°: Desahucio escrito del empleador'),
        ('20', 'Art. 163 Bis: Procedimiento concursal de liquidación'),
        ('24', 'Art. 160 N°1 Letra A): Falta de probidad'),
        ('25', 'Art. 160 N°1 Letra B): Conductas de acoso sexual'),
        ('26', 'Art. 160 N°1 Letra C): Vías de hecho'),
        ('27', 'Art. 160 N°1 Letra D): Injurias'),
        ('28', 'Art. 160 N°1 Letra E): Conducta inmoral'),
        ('29', 'Art. 160 N°1 Letra F): Conductas de acoso laboral'),
    ], string="Cláusula de Término")

    colacion_mensual = fields.Float(string="Colación Mensual")
    colacion_diaria = fields.Float(string="Colación Diaria")
    movilizacion_mensual = fields.Float(string="Movilización Mensual")
    movilizacion_diaria = fields.Float(string="Movilización Diaria")

    tipo_jornada = fields.Selection([
        ('101', 'Ordinaria-Art. 22'),
        ('201', 'Parcial-Art. 40 Bis'),
        ('301', 'Extraordinaria-Art. 30'),
        ('401', 'Especial-Art 38 Inciso 5'),
        ('402', 'Especial-Art. 23'),
        ('403', 'Especial-Art. 106'),
        ('404', 'Especial-Art. 152 Ter D'),
        ('405', 'Especial-Art. 152 Ter F'),
        ('406', 'Especial-Art. 25'),
        ('407', 'Especial-Art. 25 Bis'),
        ('408', 'Especial-Art. 149'),
        ('409', 'Especial-Art. 149 Inciso 2'),
        ('410', 'Especial-Art. 152 Bis'),
        ('411', 'Especial-Art. 36 145-D'),
        ('412', 'Especial-Art. 22 Inciso Final'),
        ('501', 'Bisemanal-Art. 149 Inciso 2'),
        ('601', 'Jornada Excepcional-Art. 38 Inciso Final'),
        ('701', 'Exenta-Art. 22'),
    ], string="Tipo de Jornada")

    region = fields.Selection([
        ('1', 'Tarapacá'),
        ('2', 'Antofagasta'),
        ('3', 'Atacama'),
        ('4', 'Coquimbo'),
        ('5', 'Valparaíso'),
        ('6', 'Libertador General Bernardo OHiggins'),
        ('7', 'Maule'),
        ('8', 'Biobío'),
        ('9', 'Araucanía'),
        ('10', 'Los Lagos'),
        ('11', 'Aysén'),
        ('12', 'Magallanes'),
        ('13', 'Metropolitana'),
        ('14', 'Los Ríos'),
        ('15', 'Arica y Parinacota'),
        ('16', 'Ñuble'),
    ], string="Región")

    comuna_id = fields.Char(string="Comuna")

    horas_trabajadas = fields.Selection([
        ('180', '180'),
        ('168', '168'),
        ('144', '144'),
        ('120', '120'),
        ('100', '100'),
        ('80', '80'),
        ('60', '60'),
        ('40', '40'),
        ('20', '20'),
    ], string="Horas Trabajadas")

    dias_semana_part_time = fields.Selection([
        ('1', 'Lunes'),
        ('2', 'Martes'),
        ('3', 'Miércoles'),
        ('4', 'Jueves'),
        ('5', 'Viernes'),
        ('6', 'Sábado'),
        ('7', 'Domingo'),
        ('0', 'Ninguno'),
    ], string="Días de la semana Part Time")

    usar_sueldo_minimo = fields.Selection([
        ('S', 'Sí'),
        ('N', 'No'),
    ], string="Usar Sueldo Mínimo", default='N')

    factor_especial_horas_extra = fields.Float(
        string="Factor Especial Horas Extra (Valor Normal)",
        default=0.00795454
    )

    porc_trabajo_pesado_trab = fields.Float(
        string='Porcentaje Trabajo Pesado Trabajador',
        default=0.0
    )
    
    porc_trabajo_pesado_emp = fields.Float(
        string='Porcentaje Trabajo Pesado Empleador',
        default=0.0
    )
    
    pensionado_invalidez = fields.Selection([
        ('0', 'NO'),
        ('1', 'DISCAPACIDAD CERTIFICADA POR LA COMPIN'),
        ('2', 'ASIGNATARIO PENSIÓN POR INVALIDEZ TOTAL'),
        ('3', 'PENSIONADO CON INVALIDEZ PARCIAL')
    ], string='Persona con Discapacidad - Pensionado por Invalidez',
        default='0'
    )
    
    vacaciones_progresivas = fields.Integer(
        string='Días Vacaciones Progresivas',
        default=0
    )
    
    vacaciones_progresivas_anio = fields.Integer(
        string='Años para Iniciar Vacaciones Progresivas',
        default=0
    )
    
    tec_extranjero = fields.Selection([
        ('0', 'NO'),
        ('1', 'SI')
    ], string='Técnico Extranjero Exención Cot. Previsionales',
        default='0'
    )
    
    tiene_ficha_covid = fields.Boolean(
        string='Ficha Covid',
        default=False
    )
    
    banco = fields.Selection([
        ('000', 'SIN BANCO'),
        ('001', 'BANCO DE CHILE'),
        ('009', 'BANCO INTERNACIONAL'),
        ('012', 'BANCO DEL ESTADO DE CHILE'),
        ('014', 'SCOTIABANK CHILE'),
        ('016', 'BANCO DE CREDITO E INVERSIONES'),
        ('027', 'CORPBANCA'),
        ('028', 'BANCO BICE'),
        ('031', 'HSBC BANK'),
        ('037', 'BANCO SANTANDER-CHILE'),
        ('039', 'BANCO ITAÚ CHILE'),
        ('049', 'BANCO SECURITY'),
        ('051', 'BANCO FALABELLA'),
        ('052', 'DEUTSCHE BANK'),
        ('053', 'BANCO RIPLEY'),
        ('054', 'RABOBANK CHILE'),
        ('055', 'BANCO CONSORCIO'),
        ('056', 'BANCO PENTA'),
        ('057', 'BANCO PARIS'),
        ('504', 'BBVA BANCO BILBAO VIZCAYA ARGENTARIA'),
        ('672', 'Coop del Pers. de la Uni. Chile LTDA')
    ], string='Banco',
        default='000'
    )
    
    numero_cuenta = fields.Char(
        string='Número de Cuenta',
        size=160
    )
    
    zona_extrema = fields.Selection([
        ('S', 'SI'),
        ('N', 'NO')
    ], string='Es Zona Extrema',
        default='N'
    )

    @api.depends('nombre', 'apellido_paterno', 'apellido_materno')
    def _compute_name(self):
        for record in self:
            partes = filter(None, [record.nombre, record.apellido_paterno, record.apellido_materno])
            record.name = ' '.join(partes)
    
    @api.depends('nombre', 'apellido_paterno', 'apellido_materno')
    def _compute_nombre_completo(self):
        for record in self:
            partes = filter(None, [record.nombre, record.apellido_paterno, record.apellido_materno])
            record.nombre_completo = ' '.join(partes)

    @api.model
    def create(self, vals):
        vals = self._capitalize_fields(vals)
        
        if 'name' not in vals:
            nombre = vals.get('nombre', '')
            apellido_paterno = vals.get('apellido_paterno', '')
            apellido_materno = vals.get('apellido_materno', '')
            partes = filter(None, [nombre, apellido_paterno, apellido_materno])
            vals['name'] = ' '.join(partes)
        
        return super(HrEmployee, self).create(vals)

    def write(self, vals):
        vals = self._capitalize_fields(vals)
        
        if any(field in vals for field in ['nombre', 'apellido_paterno', 'apellido_materno']):
            for record in self:
                nombre = vals.get('nombre', record.nombre)
                apellido_paterno = vals.get('apellido_paterno', record.apellido_paterno)
                apellido_materno = vals.get('apellido_materno', record.apellido_materno)
                partes = filter(None, [nombre, apellido_paterno, apellido_materno])
                vals['name'] = ' '.join(partes)
        
        return super(HrEmployee, self).write(vals)

    def _capitalize_fields(self, vals):
        fields_to_capitalize = [
            'nombre', 'apellido_paterno', 'apellido_materno',
            'direccion', 'comuna', 'nacionalidad', 'cargo', 'fun_isapre',
            'comuna_id', 'centro_costo_nombre'
        ]
        
        for field in fields_to_capitalize:
            if field in vals and isinstance(vals[field], str) and vals[field].strip():
                vals[field] = ' '.join(word.capitalize() for word in vals[field].split())
        
        return vals

    @api.onchange('nombre', 'apellido_paterno', 'apellido_materno', 
                  'direccion', 'comuna', 'nacionalidad', 'cargo', 'fun_isapre',
                  'comuna_id', 'centro_costo_nombre')
    def _onchange_capitalize_fields(self):
        fields_to_capitalize = [
            'nombre', 'apellido_paterno', 'apellido_materno',
            'direccion', 'comuna', 'nacionalidad', 'cargo', 'fun_isapre',
            'comuna_id', 'centro_costo_nombre'
        ]
        
        for field in fields_to_capitalize:
            value = getattr(self, field)
            if value and isinstance(value, str) and value.strip():
                capitalized_value = ' '.join(word.capitalize() for word in value.split())
                setattr(self, field, capitalized_value)


    def generar_anexo_contrato_pdf(self):
        return self.env.ref('eleccom.action_report_anexo_contrato').report_action(self)
    
    def generar_contrato_indefinido_pdf(self):
        return self.env.ref('eleccom.action_report_indefinido_contrato').report_action(self)
    
    @api.onchange('rut')
    def _onchange_rut(self):
        if self.rut:
            rut_clean = re.sub(r'[^\dkK]', '', self.rut.upper())
            
            if len(rut_clean) >= 2:
                numero = rut_clean[:-1]
                dv = rut_clean[-1]
                
                numero_formateado = self._formatear_numero_rut(numero)
                self.rut = f"{numero_formateado}-{dv}"
    
    def _formatear_numero_rut(self, numero):
        numero_revertido = numero[::-1]
        partes = []
        
        for i in range(0, len(numero_revertido), 3):
            partes.append(numero_revertido[i:i+3])
        
        numero_formateado = '.'.join(partes)[::-1]
        return numero_formateado
    
    @api.constrains('rut')
    def _check_rut(self):
        for record in self:
            if record.rut:
                if not self._validar_rut(record.rut):
                    raise ValidationError("El RUT ingresado no es válido")
    
    def _validar_rut(self, rut):
        try:
            rut = rut.upper().replace('.', '').replace('-', '')
            numero = rut[:-1]
            dv = rut[-1]
            
            if not numero.isdigit():
                return False
            
            return self._calcular_dv(numero) == dv
        except:
            return False
    
    def _calcular_dv(self, numero):
        factores = [2, 3, 4, 5, 6, 7, 2, 3]
        suma = 0
        numero = numero[::-1]
        
        for i in range(len(numero)):
            suma += int(numero[i]) * factores[i % 8]
        
        resto = suma % 11
        dv = 11 - resto
        
        if dv == 10:
            return 'K'
        elif dv == 11:
            return '0'
        else:
            return str(dv)