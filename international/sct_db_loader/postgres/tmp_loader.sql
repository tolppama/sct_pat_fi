/* Generated Loader Script */

set schema 'snomedct';

COPY concept_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/sct2_Concept_Full_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY description_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/sct2_Description_Full-en_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY stated_relationship_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/sct2_StatedRelationship_Full_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY relationship_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/sct2_Relationship_Full_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY textdefinition_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/sct2_TextDefinition_Full-en_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY attributevaluerefset_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/der2_cRefset_AttributeValueFull_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY langrefset_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/der2_cRefset_LanguageFull-en_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

COPY associationrefset_f
FROM '/Users/matiastolppanen/SNOMED_CT/international/snomed-database-loader/PostgreSQL/tmp_extracted/der2_cRefset_AssociationFull_INT_20230131.txt'
WITH (FORMAT csv, HEADER true, DELIMITER E'	', QUOTE E'');

