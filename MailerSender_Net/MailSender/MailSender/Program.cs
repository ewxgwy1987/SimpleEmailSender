using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;


namespace MailSender
{
    class Program
    {
        static void Main(string[] args)
        {
            EmailSender emailsender = new EmailSender();
            emailsender.SendEmail();

            Console.Read();
        }

        
    }
}
