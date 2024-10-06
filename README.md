# Herramientas DNIe Peru

[English](#peru-dnie-tools)

Peru DNIe es una aplicación de línea de comandos diseñada para facilitar las
operaciones criptográficas utilizando el Documento Nacional de Identidad
electrónico peruano (DNI) versión 2.

## Antes de comenzar
Esta aplicación es actualmente compatible solo con distribuciones Linux. Para
usar tu DNIe, necesitarás un lector de SmartCard o NFC USB. La mayoría de los lectores
disponibles en AliExpress son compatibles. He usado con éxito el [lector
ZoweeTek](https://es.aliexpress.com/item/32222806111.html?spm=a2g0o.detail.pcDetailBottomMoreOtherSeller.18.34d1RvABRvABIW&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40050.354490.0&scm_id=1007.40050.354490.0&scm-url=1007.40050.354490.0&pvid=4b0b3ecc-022f-4424-99ea-077d1f5a0ced&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40050.354490.0,pvid:4b0b3ecc-022f-4424-99ea-077d1f5a0ced,tpp_buckets:668%232846%238110%231995&isseo=y&pdp_npi=4%40dis%21PEN%2142.04%2110.30%21%21%2110.90%212.67%21%402101e7f617098241588065532ec86d%2112000031130620577%21rec%21PE%21%21AB&utparam-url=scene%3ApcDetailBottomMoreOtherSeller%7Cquery_from%3A) y
[lector ACR122U](https://es.aliexpress.com/item/1005007104130963.html?spm=a2g0o.order_list.order_list_main.5.3446194dYLfYqG&gatewayAdapt=glo2esp).

Para instalar este paquete, ejecuta:
```console
pip install git+https://github.com/edeustua/peru-dnie.git
```

Esto debería instalar peru-dnie junto con sus dependencias: `attrs`, `pyscard` y `rich`.

## Extrayendo tu Certificado de Firma Pública x509
El certificado público x509 contiene tu clave pública RSA, firmada por Reniec.
Esta clave verifica tu identidad y se utiliza para autenticar tus firmas
digitales.

Para extraer el certificado público de tu DNIe v2, asegúrate de que tu DNIe esté
insertado en el lector y ejecuta:

```console
peru_dnie extract signature mi_certificado_de_firma.crt
```

Este comando genera un archivo llamado `mi_certificado_de_firma.crt`, que
contiene tu certificado x509 y clave pública.

Para ver el contenido del archivo, utiliza el siguiente comando `openssl`:


```console
openssl x509 -in mi_certificado_de_firma.crt -noout -text
```

Deberías ver una salida similar a esta:

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            36:e9:0e:66:7f:9c:ff:ee:db:5b:eb:44:7e:33:87:77:15:b5:a3:09
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=PE, O=Registro Nacional de Identificación y Estado Civil, CN=ECEP-RENIEC CA Class 2 II
        Validity
            Not Before: Dec 13 14:11:52 2023 GMT
            Not After : Dec 12 14:11:52 2027 GMT
        Subject: C=PE, ST=Lima-Lima, L=San Bartolo, OU=EREP_PN_RENIEC_26468450, SN=DEUSTUA STAHR, GN=JORGE EMILIANO, serialNumber=PNOPE-********, CN=DEUSTUA STAHR JORGE EMILIANO FIR ******** hard

...
```

Para extraer la clave pública del certificado, ejecuta:

```console
openssl x509 -pubkey -noout -in mi_certificado_de_firma.crt > mi_llave_publica.pem
```

Necesitaremos esto para verificar nuestra firma en el siguiente paso.


## Firmando un archivo con tu DNIe

**NOTA**: Firmar un archivo tiene carácter legalmente vinculante. Asegúrate de
estar de acuerdo con el contenido antes de firmar.

Para demostración, vamos a firmar un archivo llamado `declaracion.txt`, que contiene la siguiente declaración:

`declaracion.txt` con el siguiente contenido:

```
Por la presente, declaro que este software es de código abierto.
```

```console
peru_dnie sign declaracion.txt declaracion.txt.firma

DNIe V2 encontrado
Por favor, introduce tu PIN:
```

Introduce el PIN que configuraste con tu DNIe. El comando produce un archivo
llamado `declaracion.txt.sig`, sirviendo como evidencia de tu firma en
`declaracion.txt`.

Para verificar tu firma, puedes ejecutar este comando `openssl`:

```console
openssl dgst -sha256 -verify mi_llave_publica.pem -signature declaracion.txt.firma declaracion.txt
```

---

## Peru DNIe tools

Peru DNIe is a CLI application designed to facilitate cryptographic operations
using the Peruvian electronic National Identity Document (DNI) version 2.

## Getting started

This application is currently compatible only with Linux distributions. To use
your DNIe, you will need a USB SmartCard or NFC reader. Most readers available on
AliExpress are compatible. I have successfully used the [ZoweeTek](https://es.aliexpress.com/item/32222806111.html?spm=a2g0o.detail.pcDetailBottomMoreOtherSeller.18.34d1RvABRvABIW&gps-id=pcDetailBottomMoreOtherSeller&scm=1007.40050.354490.0&scm_id=1007.40050.354490.0&scm-url=1007.40050.354490.0&pvid=4b0b3ecc-022f-4424-99ea-077d1f5a0ced&_t=gps-id:pcDetailBottomMoreOtherSeller,scm-url:1007.40050.354490.0,pvid:4b0b3ecc-022f-4424-99ea-077d1f5a0ced,tpp_buckets:668%232846%238110%231995&isseo=y&pdp_npi=4%40dis%21PEN%2142.04%2110.30%21%21%2110.90%212.67%21%402101e7f617098241588065532ec86d%2112000031130620577%21rec%21PE%21%21AB&utparam-url=scene%3ApcDetailBottomMoreOtherSeller%7Cquery_from%3A) and
[ACR122U](https://es.aliexpress.com/item/1005007104130963.html?spm=a2g0o.order_list.order_list_main.5.3446194dYLfYqG&gatewayAdapt=glo2esp) successfully.

To install this package, run:

```console
pip install git+https://github.com/edeustua/peru-dnie.git
```
This should install `peru-dnie` along with its dependencies: `attrs`, `pyscard` and `rich`.

## Extracting Your Public x509 Signing Certificate

The public x509 certificate contains your public RSA key, signed by Reniec. This
key verifies your identity and is used to authenticate your digital signatures.

To extract the public certificate from your DNIe v2, ensure your DNIe is
inserted into the reader and run:
```console
peru_dnie extract signature my_signing_certificate.crt
```

This command generates a file named `my_signing_certificate.crt`, containing
your x509 certificate and public key.

To view the file contents, use the following `openssl` command:

```console
openssl x509 -in my_signing_certificate.crt -noout -text
```

You should see output similar to this:
```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            36:e9:0e:66:7f:9c:ff:ee:db:5b:eb:44:7e:33:87:77:15:b5:a3:09
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=PE, O=Registro Nacional de Identificación y Estado Civil, CN=ECEP-RENIEC CA Class 2 II
        Validity
            Not Before: Dec 13 14:11:52 2023 GMT
            Not After : Dec 12 14:11:52 2027 GMT
        Subject: C=PE, ST=Lima-Lima, L=San Bartolo, OU=EREP_PN_RENIEC_26468450, SN=DEUSTUA STAHR, GN=JORGE EMILIANO, serialNumber=PNOPE-********, CN=DEUSTUA STAHR JORGE EMILIANO FIR ******** hard

...
```

To extract the public key from the certificate, execute:
```console
openssl x509 -pubkey -noout -in my_signing_certificate.crt > my_signing_pubkey.pem

```

We will need this to verify our signature in the next step.

## Signing a file with your DNIe

**NOTE**: Signing a file is legally binding. Ensure you agree with the contents
before signing.

For demonstration, let's sign a file named `statement.txt`, which contains the
following declaration:
`statement.txt` with the follwing content:

```
Hereby, I state that this software is open source.
```

Execute the following command to generate a digital signature:

```console
peru_dnie sign statement.txt statement.txt.sig

DNIe V2 encontrado
Por favor, introduce tu PIN:
```

Enter the PIN you set up with your DNIe. The command produces a file named
`statement.txt.sig`, serving as evidence of your signature on `statement.txt`.

To verify your signature, you can run this `openssl` command:
```console
openssl dgst -sha256 -verify my_signing_pubkey.pem -signature statement.txt.sig statement.txt
```

## Sources
- <https://serviciosportal.reniec.gob.pe/portalciudadano/>
