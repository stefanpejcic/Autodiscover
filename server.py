import re
from http.server import BaseHTTPRequestHandler, HTTPServer

# By David Mercereau
# Licence Beerware

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def extract_domain(self, domain):
        match = re.search(r"(?P<domain>[a-z0-9][a-z0-9\-]{1,63}\.[a-z\.]{2,6})$", domain, re.IGNORECASE)
        if match:
            return match.group('domain')
        return domain

    def do_GET(self):
        domain = self.extract_domain(self.headers['Host'])
        mail_server = f"mail.{domain}"
        
        if self.path == "/mail/config-v1.1.xml":
            self.send_response(200)
            self.send_header('Content-Type', 'application/xml')
            self.end_headers()
            
            config_xml = f'''<?xml version="1.0" encoding="utf-8" ?>
            <clientConfig version="1.1">
                <emailProvider id="{domain}">
                  <domain>{domain}</domain>
                  <displayName>{domain}</displayName>
                  <displayShortName>{domain}</displayShortName>
                  <incomingServer type="imap">
                     <hostname>{mail_server}</hostname>
                     <port>143</port>
                     <socketType>STARTTLS</socketType>
                     <username>%EMAILADDRESS%</username>
                     <authentication>password-cleartext</authentication>
                  </incomingServer>
                  <outgoingServer type="smtp">
                     <hostname>{mail_server}</hostname>
                     <port>587</port>
                     <socketType>STARTTLS</socketType>
                     <username>%EMAILADDRESS%</username>
                     <authentication>password-cleartext</authentication>
                  </outgoingServer>
                  <documentation url="https://webmail.{domain}">
                      <descr lang="fr">Connexion Webmail</descr>
                      <descr lang="en">Webmail connection</descr>
                  </documentation>
                  <documentation url="http://projet.retzo.net/projects/hebergement/wiki">
                    <descr lang="fr">Documentation</descr>
                    <descr lang="en">Generic settings page</descr>
                  </documentation>
                </emailProvider>
            </clientConfig>'''
            self.wfile.write(config_xml.encode('utf-8'))
            
        else:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        domain = self.extract_domain(self.headers['Host'])
        mail_server = f"mail.{domain}"

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Extract email address from POST data
        email_match = re.search(r"<EMailAddress>(.*?)</EMailAddress>", post_data)
        email_address = email_match.group(1) if email_match else ''

        if self.path == "/autodiscover/autodiscover.xml":
            self.send_response(200)
            self.send_header('Content-Type', 'application/xml')
            self.end_headers()

            autodiscover_xml = f'''<?xml version="1.0" encoding="utf-8" ?>
            <Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006">
               <Response xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a">
                   <Account>
                       <AccountType>email</AccountType>
                       <Action>settings</Action>
                       <Protocol>
                           <Type>IMAP</Type>
                           <Server>{mail_server}</Server>
                           <Port>993</Port>
                           <DomainRequired>off</DomainRequired>
                           <LoginName>{email_address}</LoginName>
                           <SPA>off</SPA>
                           <SSL>on</SSL>
                           <AuthRequired>on</AuthRequired>
                       </Protocol>
                       <Protocol>
                           <Type>POP3</Type>
                           <Server>{mail_server}</Server>
                           <Port>995</Port>
                           <DomainRequired>off</DomainRequired>
                           <LoginName>{email_address}</LoginName>
                           <SPA>off</SPA>
                           <SSL>on</SSL>
                           <AuthRequired>on</AuthRequired>
                       </Protocol>
                       <Protocol>
                           <Type>SMTP</Type>
                           <Server>{mail_server}</Server>
                           <Port>587</Port>
                           <DomainRequired>off</DomainRequired>
                           <LoginName>{email_address}</LoginName>
                           <SPA>off</SPA>
                           <Encryption>TLS</Encryption>
                           <AuthRequired>on</AuthRequired>
                           <UsePOPAuth>off</UsePOPAuth>
                           <SMTPLast>off</SMTPLast>
                       </Protocol>
                   </Account>
               </Response>
            </Autodiscover>'''
            self.wfile.write(autodiscover_xml.encode('utf-8'))
        else:
            self.send_error(404, "File Not Found")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run(port=8000)
  
