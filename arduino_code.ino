#include <SoftwareSerial.h>
#include <PN532_SWHSU.h>
#include <PN532.h>

SoftwareSerial SWSerial(3, 2); // RX, TX
PN532_SWHSU pn532swhsu(SWSerial);
PN532 nfc(pn532swhsu);

byte nuidPICC[4];

void setup()
{
    Serial.begin(115200);
    nfc.begin();

    uint32_t versiondata = nfc.getFirmwareVersion();
    if (!versiondata)
    {
        Serial.println("Didn't find PN53x module");
        while (1)
            ; // halt
    }

    nfc.SAMConfig();
    Serial.println("Ready to scan cards...");
}

void loop()
{
    readNFC();
}

void readNFC()
{
    uint8_t uid[] = {0, 0, 0, 0, 0, 0, 0};
    uint8_t uidLength;
    bool success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, uid, &uidLength);

    if (success)
    {
        String tagId = "";
        for (uint8_t i = 0; i < uidLength; i++)
        {
            tagId += String(uid[i]);
            if (i < uidLength - 1)
                tagId += ".";
        }

        Serial.println(tagId); // Send UID to PC
        delay(1000);
    }
}
