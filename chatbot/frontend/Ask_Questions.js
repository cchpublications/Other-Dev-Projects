exports.handler = function(context, event, callback) {
  let questions = [
    {
      "question": {
        "say": "What is your first name?"
      },
      "name": "first_name",
      "type": "Twilio.FIRST_NAME"
    },
    {
      "question": {
        "say": "What is your last name?"
      },
      "name": "last_name",
      "type": "Twilio.LAST_NAME"
    },
    {
      "question": {
        "say": "What is your preferred housing type? Please choose from: emergency shelters, coordinated entry system,  transitional housing, veterans housing, domestic violence shelters, sober living, or maternity shelters"
      },
      "name": "housing_type",
      "type": "HOUSINGTYPE"
    },
    {
      "question": {
        "say": "What is your age?"
      },
      "name": "age",
      "type": "AGE"
    },
    {
      "question": {
        "say": "What is fits your population the best? Please choose from LGBTQ, Foster Youth, Veterans, or HIV+"
      },
      "name": "population",
      "type": "UNIQUE_POPULATION"
    },
    {
      "question": {
        "say": "What is your gender?"
      },
      "name": "gender",
      "type": "GENDER"
    }
  ];
  
  let responseObject = {
    "actions": [
      {
        "collect": {
          "name": "ask_questions",
          "questions": questions,
          "on_complete": {
            "redirect": "task://test_evaluate_answers"
          }
        }
      }
    ]
  }
  
  callback(null, responseObject);
};