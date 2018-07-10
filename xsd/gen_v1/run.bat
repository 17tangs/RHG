set types=Award.txt BedType.txt CardImageTextLink.txt ContactCard.txt ContactInfo.txt Coordinates.txt EmailbyCountry.txt FacebookMetas.txt FaxbyCountry.txt Link.txt MaxOccupancy.txt Menu.txt PhoneNumberbyCountry.txt Poi.txt SpecialCard.txt Tab.txt TextContactInfo.txt TextDescription.txt TextHotel.txt TextMultimedia.txt TextOffer.txt TextRestaurant.txt TextRoom.txt TextSpecialCard.txt TextTitle.txt TextTitleBulletList.txt TextTitleDescription.txt TextTitleSubtitle.txt Time.txt TwitterMetas.txt Gallery.txt
FOR %%A IN (%types%) DO python gen.py %%A 1

set entities=AttractionList.txt AwardsAndRecognitions.txt CardList.txt Contact.txt EntityMenu.txt GalleryList.txt Hotel.txt HTA.txt ImageTextLink.txt MEFeatures.txt MultimediaText2.txt MultimediaTextLinks.txt OfferList.txt Restaurant.txt Room.txt RoomList.txt SocialMedia.txt SEO.txt Tabs.txt TextLinks.txt TripadvisorTextLink.txt

FOR %%B IN (%entities%) DO python gen.py %%B 2

PAUSE