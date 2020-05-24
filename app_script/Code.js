function moveFiles(sourceFileId, folder_name) {

  var folders = DriveApp.getFoldersByName(folder_name)
  var folder = null;
  while (folders.hasNext()) {
    folder = folders.next();
    Logger.log(folder.getName());
  }

  if (!folder)
    folder = DriveApp.createFolder(folder_name)

  var targetFolderId = folder.getId();

  Logger.log("***", targetFolderId, folder.getName())

  var file = DriveApp.getFileById(sourceFileId);
  file.getParents().next().removeFile(file);
  DriveApp.getFolderById(targetFolderId).addFile(file);
}

function createQuiz(name, desc, user, item_list, type) {

  sample_forms = ['1Yj55-xMTA9nYnatXb7SxjajrFIw_zCI_SW6TC1o1sXs'];
  var file = DriveApp.getFileById(sample_forms[type]);
  file = file.makeCopy(name)
  var form = FormApp.openById(file.getId());

  //var form = FormApp.create(name);
  form.deleteAllResponses()
  form.deleteItem(0)


  form.setTitle(name);
  //form.setLimitOneResponsePerUser(true);
  form.setIsQuiz(true);
  form.setConfirmationMessage("Good job!")
  var folder_name = null;
  if (desc)
    form.setDescription(desc)

  if (user && user.email) {
    form.addEditor(user.email)
    folder_name = user.email + "&" + user.givenName;
  }

  form.setPublishingSummary(true)
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
    if (ques.desc) {
        item.setHelpText(ques.desc);
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


    //var textValidation = FormApp.createTextValidation()
    //  .setHelpText(“Input was not a number between 1 and 100.”)
    //  .requireNumberBetween(1, 100);
    //textItem.setValidation(textValidation);
  }


  var metadata = {
    id: form.getId(),
    count_items: item_list.length,
    total_points: total_points,
    published_url: form.getPublishedUrl(),
    editor_url: form.getEditUrl(),
    // destination_id: form.getDestinationId(),
    editors: form.getEditors(),
    summary_url: form.getSummaryUrl(),
    //updated: file.getLastUpdated().toJSON(),
    //created: file.getDateCreated().toJSON()
  }
  response = {
    title: form.getTitle(),
    description: form.getDescription(),
    metadata: metadata,
    id: form.getId()
  }
  Logger.log(response)
  if (folder_name)
    moveFiles(form.getId(), folder_name)
  else
    moveFiles(form.getId(), 'User Forms')

  return(response)

}

function getQuizDetails(form_url, get_responses) {
  // Open a form by URL.
  var form = FormApp.openByUrl(form_url);
  var items = form.getItems();
  item_list = []
  var total_points = 0;
  var count_items = 0;
  for (var i = 0; i < items.length; i++) {
    var choices_list = [];
    var points = null;
    var feedback_correct = null;
    var feedback_incorrect = null;
    var item = items[i];
    var answer = ""
    var type = item.getType()

    if (type == 'MULTIPLE_CHOICE' || type == 'CHECKBOX') {
      var q_item = (type == 'MULTIPLE_CHOICE' ? item.asMultipleChoiceItem() : item.asCheckboxItem());
      points = q_item.getPoints();
      if (!points || points==0) continue;
      var options = q_item.getChoices()
      var token = ""

      total_points += points;
      feedback_correct = q_item.getFeedbackForCorrect() ? q_item.getFeedbackForCorrect().getText() : null
      feedback_incorrect = q_item.getFeedbackForIncorrect() ? q_item.getFeedbackForIncorrect().getText() : null
      count_items++;
      for (var j = 0; j < options.length; j++) {
          var chs = {choice: options[j].getValue(), correct: options[j].isCorrectAnswer() ? 1: 0}
          choices_list.push(chs)
          if (options[j].isCorrectAnswer()) {
            answer = answer + token + options[j].getValue();
            token = ";";
          }
      }
    }
    item_list.push({title: item.getTitle(),
               description: item.getHelpText(),
               type: type,
               choices: choices_list,
               answer: answer,
               points: points,
               feedback_correct: feedback_correct,
               feedback_incorrect: feedback_incorrect
             })
  }
  //Logger.log(item_list)
  responses = []
  var formResponses = form.getResponses();
  if (get_responses) {
    for (var i = 0; i < formResponses.length; i++) {
      var formResponse = formResponses[i];
      var itemResponses = formResponse.getItemResponses();
      for (var j = 5; j < itemResponses.length; j++) {
        var itemResponse = itemResponses[j];
        Logger.log('Response #%s to the question "%s" was "%s [%s] -> {%s}"',
            (i + 1).toString(),
            itemResponse.getItem().getTitle(),
            itemResponse.getResponse(),
            itemResponse.getScore(),
            itemResponse.getItem().asMultipleChoiceItem().getChoices()[0].getValue()
            );
      }
    }
  }
  var file = DriveApp.getFileById(form.getId());
  var metadata = {
    id: form.getId(),
    count_items: parseInt(count_items),
    total_points: total_points,
    published_url: form.getPublishedUrl(),
    editor_url: form.getEditUrl(),
    destination_id: form.getDestinationId(),
    editors: form.getEditors(),
    summary_url: form.getSummaryUrl(),
    updated: file.getLastUpdated().toJSON(),
    created: file.getDateCreated().toJSON()
  }
  response = {
    title: form.getTitle(),
    description: form.getDescription(),
    items: item_list,
    responses_count: parseInt(formResponses.length),
    responses: responses,
    metadata: metadata
  }
  Logger.log(response)
  return(response)

}

function testFunction() {
   getQuizDetails('https://docs.google.com/forms/d/1eJgoRzOq00jv2D32Jyav7o6cElJ9sdORU_oUrJQj69c/edit', false)
}

function testFunction2() {
   var question_list = [
     {'question': "name?", "options": [{"correct": 0, "choice": "123"}, {"correct": 0,"choice": "11123"}, {"correct": 1,"choice": "123123"},{"correct": 0,"choice": "234234"}], desc: 'Quran', type:'MULTIPLE_CHOICE', points: 2},
     {'question': "name2?", "options": [{"correct": 0, "choice": "123"}, {"correct": 1,"choice": "1253"}, {"correct": 0,"choice": "123123"},{"correct": 0,"choice": "234234"}], type:'MULTIPLE_CHOICE', required: false},
     {'question': "name3?", "options": [{"correct": 0, "choice": "A"}, {"correct": 1,"choice": "B"}, {"correct": 0,"choice": "C"},{"correct": 0,"choice": "D"}, {"correct": 1,"choice": "E"}], type:'CHECKBOX', feedback_correct: 'Very good!'},
   ]
   var user = {email: 'farrukh503@gmail.com', givenName: 'Farrukh'};
   createQuiz("RM Form 5", "Summary of features", user, question_list, 0)
}
