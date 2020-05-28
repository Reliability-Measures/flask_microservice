QUIZ_CODE = '''
function createQuiz(name, desc, user, item_list, options) {
   // to keep the format and options not settable by the script
  sample_forms = [
    '1HvsLyFZlrAaOFJFhn5u-zcYnIXEXp4A7e5ElBZGSNfI', // correct answer hide
    '102l6S_GF172zfFx3d2gcWNHF1Bv3N6KcDQfXwQsBAgg' // correct answer show
  ]; 
  type = 0;
  //Logger.log(options)
  if (options.show_correct) type=1;  // correct answer show
  
  var file = DriveApp.getFileById(sample_forms[type]);
  file = file.makeCopy(name)
  var form = FormApp.openById(file.getId());
  
  //var form = FormApp.create(name);
  form.deleteAllResponses()
  
  if (!options.name)
    form.deleteItem(0)  // name
      
  
  form.setTitle(name);
  //form.setLimitOneResponsePerUser(true);
  form.setIsQuiz(true);
  form.setConfirmationMessage("Good job!")
  var folder_name = null;
  if (desc) 
    form.setDescription(desc)
  
  folder_name = null;
  if (user && user.email) {
    form.addEditor(user.email)
    folder_name = user.email + "&" + user.givenName;
  }
    
  if (options.summary) form.setPublishingSummary(true)
  total_points = 0;
  for (var i=0; i<item_list.length; i++) {
    var ques = item_list[i];
    var type = ques.type;
    var item = null;
    if (type=='MULTIPLE_CHOICE')
      item = form.addMultipleChoiceItem(); 
    if (type=='CHECKBOX')
      item = form.addCheckboxItem();
    if (type=='TEXT')
      item = form.addTextItem();
      
    if (!item) continue;  

    item.setTitle(ques.question);
    if (ques.desc || ques.description) {
        item.setHelpText(ques.desc || ques.description);
    }
    if (type == 'MULTIPLE_CHOICE' || type == 'CHECKBOX') {
      var choices = [];
      for(var j=0;j<ques.options.length; j++){
        var ch = ques.options[j]
        choices.push(item.createChoice(ch.choice, !!ch.correct))
      }
      item.setChoices(choices)
      points = ques.points || 1;
      item.setPoints(points)
      total_points += points;
      var fb = FormApp.createFeedback();
      if (ques.feedback_correct) 
        item.setFeedbackForCorrect(fb.setText(ques.feedback_correct).build())
      if (ques.feedback_incorrect)
        item.setFeedbackForIncorrect(fb.setText(ques.feedback_incorrect).build())
    }
    else {
      points = ques.points || 0;
      item.setPoints(points)
      total_points += points;          
    }
    if (ques.required==null)
      item.setRequired(true);
    else
      item.setRequired(ques.required);   
  }
 
  if (options.email) form.setCollectEmail(true)
  
  var metadata = {
    id: form.getId(),
    count_items: item_list.length,
    total_points: total_points,
    published_url: form.getPublishedUrl(),
    editor_url: form.getEditUrl(),
    // destination_id: form.getDestinationId(),
    editors: form.getEditors(),
    summary_url: form.getSummaryUrl(),
    folder_name: folder_name
    //updated: file.getLastUpdated().toJSON(),
    //created: file.getDateCreated().toJSON()    
  }  
  response = {
    title: form.getTitle(),
    description: form.getDescription(),
    metadata: metadata,
    id: form.getId()
  }
  //Logger.log(response)
  //if (folder_name)
  //  moveFiles(form.getId(), folder_name)
  //else
  //  moveFiles(form.getId(), 'User Forms')
      
  return(response)
  
}
'''.strip()

QUIZ_MANIFEST = '''
{
  "timeZone": "America/Chicago",
  "exceptionLogging": "CLOUD"
}
'''.strip()