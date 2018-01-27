%prolog

% simple home automation world

:- multifile rdfsLabel/3.
:- multifile aiHomeLocation/1.
:- multifile aiPrepLoc/3.

aiHomeLocation(aiHLAttic).
aiHomeLocation(aiHLBasement).
aiHomeLocation(aiHLBathroom).
aiHomeLocation(aiHLBedroom).
aiHomeLocation(aiHLChildrensRoom).
aiHomeLocation(aiHLDiningRoom).
aiHomeLocation(aiHLGuestRoom).
aiHomeLocation(aiHLHall).
aiHomeLocation(aiHLKitchen).
aiHomeLocation(aiHLLivingRoom).
aiHomeLocation(aiHLOffice).
aiHomeLocation(aiHLShop).
aiHomeLocation(aiHLStudy).
aiHomeLocation(aiHLUpstairs).
aiHomeLocation(aiHLWorkRoom).
aiHomeLocation(aiHLWorkshop).
aiPrepLoc(aiHLAttic, de, 'auf dem').
aiPrepLoc(aiHLAttic, en, 'in the').
aiPrepLoc(aiHLBasement, de, 'im').
aiPrepLoc(aiHLBasement, en, 'in the').
aiPrepLoc(aiHLBathroom, de, 'im').
aiPrepLoc(aiHLBathroom, en, 'in the').
aiPrepLoc(aiHLBedroom, de, 'im').
aiPrepLoc(aiHLBedroom, en, 'in the').
aiPrepLoc(aiHLChildrensRoom, de, 'im').
aiPrepLoc(aiHLChildrensRoom, en, 'in the').
aiPrepLoc(aiHLDiningRoom, de, 'im').
aiPrepLoc(aiHLDiningRoom, en, 'in the').
aiPrepLoc(aiHLGuestRoom, de, 'im').
aiPrepLoc(aiHLGuestRoom, en, 'in the').
aiPrepLoc(aiHLHall, de, 'im').
aiPrepLoc(aiHLHall, en, 'in the').
aiPrepLoc(aiHLKitchen, de, 'in der').
aiPrepLoc(aiHLKitchen, en, 'in the').
aiPrepLoc(aiHLLivingRoom, de, 'im').
aiPrepLoc(aiHLLivingRoom, en, 'in the').
aiPrepLoc(aiHLOffice, de, 'im').
aiPrepLoc(aiHLOffice, en, 'in the').
aiPrepLoc(aiHLShop, de, 'im').
aiPrepLoc(aiHLShop, en, 'in the').
aiPrepLoc(aiHLStudy, de, 'im').
aiPrepLoc(aiHLStudy, en, 'in the').
aiPrepLoc(aiHLUpstairs, de, 'im').
aiPrepLoc(aiHLUpstairs, en, '').
aiPrepLoc(aiHLWorkRoom, de, 'im').
aiPrepLoc(aiHLWorkRoom, en, 'in the').
aiPrepLoc(aiHLWorkshop, de, 'in der').
aiPrepLoc(aiHLWorkshop, en, 'in the').
rdfsLabel(aiHLAttic, de, 'Dachboden').
rdfsLabel(aiHLAttic, en, 'attic').
rdfsLabel(aiHLBasement, de, 'Keller').
rdfsLabel(aiHLBasement, en, 'basement').
rdfsLabel(aiHLBasement, en, 'cellar').
rdfsLabel(aiHLBathroom, de, 'Badezimmer').
rdfsLabel(aiHLBathroom, en, 'bathroom').
rdfsLabel(aiHLBedroom, de, 'Schlafzimmer').
rdfsLabel(aiHLBedroom, en, 'bedroom').
rdfsLabel(aiHLChildrensRoom, de, 'Kinderzimmer').
rdfsLabel(aiHLChildrensRoom, en, 'children\'s room').
rdfsLabel(aiHLDiningRoom, de, 'Esszimmer').
rdfsLabel(aiHLDiningRoom, en, 'dining room').
rdfsLabel(aiHLGuestRoom, de, 'Gästezimmer').
rdfsLabel(aiHLGuestRoom, en, 'guest room').
rdfsLabel(aiHLHall, de, 'Flur').
rdfsLabel(aiHLHall, en, 'hall').
rdfsLabel(aiHLKitchen, de, 'Küche').
rdfsLabel(aiHLKitchen, en, 'kitchen').
rdfsLabel(aiHLLivingRoom, de, 'Wohnzimmer').
rdfsLabel(aiHLLivingRoom, en, 'living room').
rdfsLabel(aiHLOffice, de, 'Büro').
rdfsLabel(aiHLOffice, en, 'office').
rdfsLabel(aiHLShop, de, 'Laden').
rdfsLabel(aiHLShop, en, 'shop').
rdfsLabel(aiHLStudy, de, 'Arbeitszimmer').
rdfsLabel(aiHLStudy, en, 'study').
rdfsLabel(aiHLUpstairs, de, 'Obergeschoss').
rdfsLabel(aiHLUpstairs, en, 'upstairs').
rdfsLabel(aiHLWorkRoom, de, 'Arbeitszimmer').
rdfsLabel(aiHLWorkRoom, en, 'work room').
rdfsLabel(aiHLWorkshop, de, 'Werkstatt').
rdfsLabel(aiHLWorkshop, en, 'workshop').
