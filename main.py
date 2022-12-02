import random


def find_match(p, list):
    match = random.choice(list)
    if match == p:
        find_match(p, list)
    return match


def send_mapping_per_mail(mapping):
    print("Password for Mail: ")
    pswd = input()

    with open("mail.txt", "r") as file:
        mailcontent = file.read()
        file.close()

    import ssl
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    import smtplib
    with smtplib.SMTP("ex-01.tgm.ac.at", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login("pelias", pswd)
        from email.message import EmailMessage

        for entry in mapping:
            msg = EmailMessage()
            msg.set_content(mailcontent.replace("%Bengerl%", mapping.get(entry)))
            msg['Subject'] = "Engerl Bengerl 2022"
            msg['From'] = "pelias@student.tgm.ac.at"
            msg['To'] = entry
            server.send_message(msg)
            from time import sleep
            sleep(15) # delay so rate limit gets bypassed :))
        server.quit()


if __name__ == '__main__':
    print("Reading Teilnehmer File.")
    file = open('teilnehmer.txt', 'r')
    teilnehmer = file.read().replace('\n', '').split(",")
    print("Found " + str(len(teilnehmer)) + " Participants.")
    teilnehmerMapping = dict()
    for Mail in teilnehmer:
        teilnehmerMapping.update({Mail: None})
    print("Participants Mapping created.")
    print("Starting shuffling process.")
    for t in teilnehmerMapping:
        accept = False
        while not accept:
            match = find_match(t, teilnehmer)
            print(t + " matched with " + match + ". Accept? (y/n)")
            accept = input() == "y"
            if accept:
                print("Accepted " + t + " : " + match + ". Popping (" + match + ").")
                teilnehmerMapping.update({t: match})
                teilnehmer.remove(match)
    print("Finished shuffling process.")
    print(teilnehmerMapping)
    open('mapping.json', 'w').write(str(teilnehmerMapping))
    print("Should this mapping be sent per Mail? (y/n)")
    if input() == "y":
        send_mapping_per_mail(teilnehmerMapping)
    else:
        print("Mapping not sent.")
    print("All Done.")
