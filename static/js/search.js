$(document).on('click', function(e){
    if (e.target.id === 'search-help'){
        Notiflix.Report.Info('מה אפשר לחפש?',
        `
        החיפוש רץ על <b>כל</b> פריט מידע שמופיע בפרופיל. <br>
        למשל, בשביל להגיע ל<b> בנימין זאב הרצל </b> אפשר:<br>
        - לחפש לפי השם " <b>זאב הרצל </b> " או " <b> הרצל </b> ". <br>
        - לחפש כל פרט שעשוי לזהות אותו. לדוגמא:<br>
         " <b> עיתונאי וינה אלטנוילנד עגבת </b> " (לא משנה הסדר) 
        `,
        'הבנתי');
    }
})

$('#search-profile').on('submit', function(e){
    Notiflix.Loading.Dots();
});