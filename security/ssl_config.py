"""
SSL/TLS configuration module for secure network communication.
Manages SSL certificate generation and configuration.
"""

import os
import ssl
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from datetime import datetime, timedelta

class SSLConfiguration:
    def __init__(
        self,
        common_name: str = 'localhost',
        days_valid: int = 365,
        output_dir: str = 'ssl_certs'
    ):
        """
        Configure SSL/TLS certificate settings.

        Args:
            common_name (str): Certificate domain/hostname
            days_valid (int): Certificate validity period
            output_dir (str): Directory to store generated certificates
        """
        self.common_name = common_name
        self.days_valid = days_valid
        self.output_dir = output_dir
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

    def generate_self_signed_cert(self):
        """
        Generate a self-signed SSL certificate.

        Returns:
            Tuple of (certificate_path, key_path)
        """
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Write private key to file
        key_path = os.path.join(self.output_dir, f'{self.common_name}_private_key.pem')
        with open(key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, u'US'),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u'California'),
            x509.NameAttribute(NameOID.LOCALITY_NAME, u'San Francisco'),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, u'My Company'),
            x509.NameAttribute(NameOID.COMMON_NAME, self.common_name)
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=self.days_valid)
        ).sign(private_key, hashes.SHA256())

        # Write certificate to file
        cert_path = os.path.join(self.output_dir, f'{self.common_name}_certificate.pem')
        with open(cert_path, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        return cert_path, key_path

    def create_ssl_context(self, cert_path: str, key_path: str) -> ssl.SSLContext:
        """
        Create an SSL context using the generated certificate.

        Args:
            cert_path (str): Path to SSL certificate
            key_path (str): Path to private key

        Returns:
            ssl.SSLContext: Configured SSL context
        """
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=cert_path, keyfile=key_path)
        return context