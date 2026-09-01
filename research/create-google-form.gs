/**
 * Myntra Wishlist User Survey — Google Form builder
 *
 * HOW TO RUN (2 minutes):
 * 1. Open https://script.google.com → New project
 * 2. Paste this entire file (replace default Code.gs contents)
 * 3. Click Run → select createMyntraWishlistSurvey → Authorize when prompted
 * 4. View → Logs — copy the published Form URL
 * 5. Optional: open the edit URL to tweak design / theme before sharing
 */

function createMyntraWishlistSurvey() {
  var form = FormApp.create(
    'How do you decide whether to buy items on your Myntra wishlist?'
  );

  form.setDescription(
    'We\u2019re researching how people use Myntra wishlist \u2014 not selling anything, no discounts involved. ' +
      'Your answers are anonymous and take about 10 minutes. There are no right or wrong answers.\n\n' +
      'By continuing, you agree that your responses may be used for an academic product research project.'
  );
  form.setCollectEmail(false);
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setConfirmationMessage(
    'Thank you for sharing your wishlist habits! Your responses help us understand how people decide what to buy.'
  );

  // --- SECTION 0: Screener ---
  form.addPageBreakItem()
    .setTitle('Eligibility')
    .setHelpText('Quick check \u2014 takes 30 seconds.');

  var q1 = form.addMultipleChoiceItem()
    .setTitle('Q1. Do you shop for fashion / clothing / footwear on Myntra?')
    .setRequired(true);
  q1.setChoices([
    q1.createChoice('Yes, regularly (at least once a month)'),
    q1.createChoice('Yes, occasionally (every few months)'),
    q1.createChoice('Rarely'),
    q1.createChoice('Never', FormApp.PageNavigationType.SUBMIT),
  ]);

  var q2 = form.addMultipleChoiceItem()
    .setTitle('Q2. Do you use the wishlist (heart / save) feature on Myntra?')
    .setRequired(true);
  q2.setChoices([
    q2.createChoice('Yes, often \u2014 I save items instead of buying immediately'),
    q2.createChoice('Yes, sometimes'),
    q2.createChoice('Rarely'),
    q2.createChoice('No, I never use wishlist', FormApp.PageNavigationType.SUBMIT),
  ]);

  form.addMultipleChoiceItem()
    .setTitle('Q3. Roughly how many items are on your Myntra wishlist right now?')
    .setRequired(true)
    .setChoices([
      '0',
      '1\u20132',
      '3\u201310',
      '11\u201330',
      '31\u2013100',
      '100+',
    ]);

  var q4 = form.addMultipleChoiceItem()
    .setTitle(
      'Q4. In the last 3 months, have you wishlisted at least one item you liked but did NOT buy?'
    )
    .setRequired(true);
  q4.setChoices([
    q4.createChoice('Yes'),
    q4.createChoice('No', FormApp.PageNavigationType.SUBMIT),
  ]);

  // --- SECTION 1: About you ---
  form.addPageBreakItem()
    .setTitle('About you')
    .setHelpText('Optional demographics \u2014 helps us understand different shopper types.');

  form.addMultipleChoiceItem()
    .setTitle('Q5. Your age group')
    .setRequired(true)
    .setChoices(['Under 20', '20\u201324', '25\u201329', '30\u201335', '36+']);

  var q6 = form.addCheckboxItem()
    .setTitle('Q6. What do you most often save to wishlist? (Select all that apply)')
    .setRequired(true)
    .setChoices([
      'Ethnic wear (kurta, saree, lehenga, etc.)',
      'Western wear (dresses, tops, jeans)',
      'Footwear',
      'Activewear',
      "Men's fashion",
      'Accessories / bags',
    ]);
  q6.showOtherOption(true);

  var q7 = form.addMultipleChoiceItem()
    .setTitle("Q7. When you save items to wishlist, it's usually because\u2026 (Pick one)")
    .setRequired(true)
    .setChoices([
      'I plan to buy it soon \u2014 just not right now',
      "I'm comparing options before deciding",
      "I'm waiting for a sale / better price",
      "It's for a specific event (wedding, festival, trip)",
      "It's a gift for someone",
      "I'm just bookmarking / mood-boarding \u2014 may never buy",
    ]);
  q7.showOtherOption(true);

  // --- SECTION 2: Wishlist behavior ---
  form.addPageBreakItem()
    .setTitle('Wishlist intent & purchase behavior')
    .setHelpText('How you actually use your saved items.');

  form.addMultipleChoiceItem()
    .setTitle('Q8. Of the items currently on your wishlist, how many do you actually expect to buy?')
    .setRequired(true)
    .setChoices([
      "None \u2014 it's mostly browsing",
      'About 25% or less',
      'About half',
      'About 75%',
      'Almost all of them',
    ]);

  form.addMultipleChoiceItem()
    .setTitle('Q9. How often do you go back and open your Myntra wishlist?')
    .setRequired(true)
    .setChoices([
      'Daily / almost daily',
      'Weekly',
      'Monthly',
      'Rarely \u2014 I forget it\u2019s there',
      'Only during sales (EORS, etc.)',
    ]);

  form.addMultipleChoiceItem()
    .setTitle('Q10. When you revisit your wishlist, what do you usually do?')
    .setRequired(true)
    .setChoices([
      'Open specific product pages again',
      'Just scroll the list without opening items',
      'Add some items to cart',
      'Remove items without buying',
      'Share items with friends/family',
      'Compare prices on other apps',
    ]);

  form.addMultipleChoiceItem()
    .setTitle(
      'Q11. In the last 30 days, did you purchase any item that was on your wishlist first?'
    )
    .setRequired(true)
    .setChoices([
      'Yes, at least one',
      'No, not yet but I still plan to',
      "No, and I probably won't buy most of them",
    ]);

  // --- SECTION 3: Blockers ---
  form.addPageBreakItem()
    .setTitle("What's stopping you?")
    .setHelpText('Pick up to 2 for Q12.');

  var q12 = form.addCheckboxItem()
    .setTitle("Q12. What stops you from buying items on your wishlist? (Select up to 2)")
    .setRequired(true)
    .setChoices([
      'Not sure about size / fit / how it will look on me',
      "Confused between multiple saved items \u2014 can't decide",
      'Waiting for sale / better price',
      'Not sure about fabric / quality from photos',
      'Worried about returns / delivery hassle',
      'I forgot why I saved it / lost interest',
    ]);
  q12.setValidation(
    FormApp.createCheckboxValidation().requireSelectBetween(1, 2).build()
  );

  form.addScaleItem()
    .setTitle(
      'Q13. How much do you agree: "I trust Myntra\u2019s size chart and reviews enough to buy wishlisted clothes without checking elsewhere"'
    )
    .setRequired(true)
    .setBounds(1, 5)
    .setLabels('Strongly disagree', 'Strongly agree');

  // --- SECTION 4: Before you buy ---
  form.addPageBreakItem()
    .setTitle('Before you buy')
    .setHelpText('External checks and saved-item overload.');

  form.addCheckboxItem()
    .setTitle(
      'Q14. Before buying something you saved on Myntra, do you check outside the app? (Select all that apply)'
    )
    .setRequired(true)
    .setChoices([
      'YouTube / Instagram try-on or haul videos',
      'Ask friends or family (WhatsApp, etc.)',
      'Compare on AJIO / Amazon / other apps',
      'Google search',
      'No \u2014 I decide only using Myntra',
    ]);

  form.addMultipleChoiceItem()
    .setTitle(
      'Q15. Do you currently have multiple similar items saved on wishlist (e.g., 3 kurtas for one wedding)?'
    )
    .setRequired(true)
    .setChoices(['Yes, often', 'Sometimes', 'Rarely', 'No']);

  // --- SECTION 5: Concept test ---
  form.addPageBreakItem()
    .setTitle('New feature idea \u2014 Confidence Brief')
    .setHelpText(
      'Imagine this: On each wishlisted item, Myntra uses AI to show a short Confidence Brief \u2014 your recommended size, ' +
        'what buyers with a similar body type said about fit, and whether it works for the occasion you had in mind. ' +
        'No extra discount \u2014 just help deciding.'
    );

  form.addMultipleChoiceItem()
    .setTitle(
      'Q16. If this existed, how likely would you be to buy more items from your wishlist?'
    )
    .setRequired(true)
    .setChoices([
      'Much more likely',
      'Somewhat more likely',
      'No change',
      'Somewhat less likely',
      'Would not use it',
    ]);

  form.addMultipleChoiceItem()
    .setTitle('Q17. Which part of the Confidence Brief would matter most to you? (Pick one)')
    .setRequired(true)
    .setChoices([
      'Size / fit recommendation for my body type',
      'Summary of what reviews say about fit',
      'Occasion suitability ("works for wedding / office / casual")',
      'Compare this item vs other items on my wishlist',
      'None of these would help',
    ]);

  form.addMultipleChoiceItem()
    .setTitle(
      'Q18. If Myntra integrated AI to solve your wishlist problems (fit uncertainty, choosing between saved items, occasion tips), would you be open to using it?'
    )
    .setRequired(true)
    .setChoices([
      "Yes \u2014 I'd use it when I'm stuck on a saved item",
      "Maybe \u2014 I'd try it but want to verify the advice first",
      'Only for size/fit \u2014 not for other decisions',
      'No \u2014 I prefer YouTube, friends, or my own judgment',
      "No \u2014 I don't trust AI for fashion purchases",
    ]);

  // --- SECTION 6: Open feedback & follow-up ---
  form.addPageBreakItem()
    .setTitle('Your story')
    .setHelpText('Open-ended \u2014 the most valuable part for us.');

  form.addParagraphTextItem()
    .setTitle(
      "Q19. Describe the last time you wishlisted something on Myntra but didn't buy it. What happened?"
    )
    .setRequired(true);

  form.addTextItem()
    .setTitle(
      'Q20. If Myntra could fix one thing about wishlist so you buy more of what you save \u2014 what would it be?'
    )
    .setRequired(true);

  form.addMultipleChoiceItem()
    .setTitle(
      'Q21. Would you be open to a 15-minute follow-up call to discuss your wishlist habits?'
    )
    .setRequired(true)
    .setChoices(['Yes', 'No thanks']);

  form.addTextItem()
    .setTitle('If yes, please share your email or phone number')
    .setRequired(false)
    .setHelpText('Only used to schedule a follow-up call. Leave blank if you selected No thanks.');

  var publishedUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();

  Logger.log('Form created successfully!');
  Logger.log('Share this link: ' + publishedUrl);
  Logger.log('Edit form here: ' + editUrl);

  return {
    publishedUrl: publishedUrl,
    editUrl: editUrl,
  };
}
