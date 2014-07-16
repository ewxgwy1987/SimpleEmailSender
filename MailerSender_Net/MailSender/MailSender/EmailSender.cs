using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using System.IO;
using System.Net.Mail;

namespace MailSender
{
    public class EmailSender
    {
        string FILE_MSG = "message.txt";
        string FILE_EMAILADDRESS = "EmailAddresses.txt";

        string SMTP_SERVER = "smtp.163.com";
        string Email_USR = "ewxgwy1987";
        string Email_PWD = "21-ewxgwy";
        string Email_FROM = "ewxgwy1987@163.com";

        int Email_Port = 25;
        bool Email_EnableSSL = false;

        string Email_Subject;
        string Email_Body;
        string[] Email_ToList;

        public EmailSender()
        {
            StreamReader sr_EmailBody = null;
            StreamReader sr_EmailTo = null;
            try
            {
                Email_Subject = "Test SVN email.";

                sr_EmailBody = File.OpenText(FILE_MSG);
                Email_Body = sr_EmailBody.ReadToEnd();

                sr_EmailTo = File.OpenText(FILE_EMAILADDRESS);
                string str_EmailToList = sr_EmailTo.ReadToEnd().Replace("\r", "");
                Email_ToList = str_EmailToList.Split('\n');

            }
            catch (Exception exp)
            {
                Console.WriteLine("EmailSender is failed to initialize");
                Console.WriteLine(exp.ToString());
            }
            finally
            {
                if (sr_EmailBody != null)
                    sr_EmailBody.Close();
                if (sr_EmailTo != null)
                    sr_EmailTo.Close();
            }
        }

        public void SendEmail()
        {
            if (Email_Subject != null && Email_Body != null && Email_ToList.Length > 0)
            {
                SendEmail(Email_Subject, Email_Body, Email_ToList);
            }
        }

        public void SendEmail(string subject, string body, string[] EmailToList)
        {
            try
            {

                MailMessage message = new MailMessage();

                message.From = new MailAddress(Email_FROM);

                foreach (string tempReceiver in EmailToList)
                {
                    message.To.Add(new MailAddress(tempReceiver));
                }

                message.Subject = subject;

                message.Body = body;

                SmtpClient client = new SmtpClient(SMTP_SERVER);
                client.Port = Email_Port;
                client.Credentials = new System.Net.NetworkCredential(Email_USR, Email_PWD);
                client.EnableSsl = Email_EnableSSL;
                client.Send(message);
            }
            catch (Exception exp)
            {
                Console.WriteLine(exp.ToString());
            }
        }
    }
}
