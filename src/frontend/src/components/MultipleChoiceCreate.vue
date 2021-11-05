<template>
  <div class="question">
    <div class="description" v-if="!select">
      <h3>Multiple Choice</h3>
      <p>A multiple choice question wtih a single answer. It is possible to add random variables to this type of question.</p>
    </div>
    <div class="description" v-if="select">
      <h3>Multiple Select</h3>
      <p>A multiple choice question wtih multiple possible answers. It is possible to add random variables to this type of question. List each correct answer in a space seperated list ('A B C F').</p>
    </div>
    <sui-form class="questionText">
        <sui-form-field>
          <label>Question Text</label>
          <input v-model="questionText" placeholder="Question Text" type="text">
        </sui-form-field>
    </sui-form>
    <sui-form class="variables">
      <h3>Variables</h3>
      <p>Add variables to questions and answers with the syntax ${var_name}. Variables can have three types - Integer Range, Decimal Range, and Discrete Set. </p> 
      <ul>
        <li>Integer Range - Inputted as "x-y", where x and y are integers, this range will only select integer values between the bounds x and y, inclusive.</li>
        <li>Decimal Range - Inputted as "x-y", where x and y are real numbers, this range will select decimal values up to the hundredths place between the bounds x and y, inclusive.</li>
        <li>Discrete Set - Inputted as "a,b,...,y,z" this range will select values only from the list provided. This variable can be used for numbers as well as strings.</li>
      </ul>
      <div class="variable" v-for="(item, index) in variableTexts" :key="index">
        <div class="name">
          <label>Variable Name</label>
          <input v-model="item.name" placeholder="Variable Name">
        </div>
        <div class="type">
          <label>Variable Type</label>
          <sui-dropdown
            placeholder="Select type of variable"
                :options="variableTypes"
                selection
                search
                v-model="item.type"
          />
        </div>
        <div class="range">
          <label>Range</label>
          <input v-model="item.range" placeholder="Range">
        </div>
      </div>
    </sui-form>
    <div class="variableButtons">
      <center>
        <button
            :class="numberOfVariables <= 0 ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                    :disabled="numberOfVariables <= 0 ? true : false"
                    :style="numberOfVariables <= 0 ? '' : returnPrimaryButtonStyle"
            data-toggle="tooltip"
            data-placement="bottom"
            title="RemoveVariable"
            @click="removeVariable()"
        >Remove Variable</button>
        <button
            :class="numberOfVariables >= 10 ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                    :disabled="numberOfVariables >= 10 ? true : false"
                    :style="numberOfVariables >= 10 ? '' : returnPrimaryButtonStyle"
            data-toggle="tooltip"
            data-placement="bottom"
            title="AddVariable"
            @click="addVariable()"
        >Add Variable</button>
      </center>
      </div>
    <sui-form class="answers">
      <div class="answer" v-for="(item, index) in answerTexts" :key="index">
        <div class="label">
          <p>{{item.label}}</p>
        </div>
        <div class="text">
          <input v-model="item.text" placeholder="Answer Text">
        </div>
      </div>
    </sui-form>
    <div class="buttons">
    <center>
      <button
          :class="numberOfAnswers <= 1 ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                  :disabled="numberOfAnswers <= 1 ? true : false"
                  :style="numberOfAnswers <= 1 ? '' : returnPrimaryButtonStyle"
          data-toggle="tooltip"
          data-placement="bottom"
          title="RemoveAnswer"
          @click="removeAnswer()"
      >Remove Answer</button>
      <button
          :class="numberOfAnswers >= 25 ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                  :disabled="numberOfAnswers >= 25 ? true : false"
                  :style="numberOfAnswers >= 25 ? '' : returnPrimaryButtonStyle"
          data-toggle="tooltip"
          data-placement="bottom"
          title="AddAnswer"
          @click="addAnswer()"
      >Add Answer</button>
    </center>
    </div>
    <div class="correct">
      <sui-form>
        <sui-form-field>
          <label v-if="select">Correct Answers</label>
          <label v-if="!select">Correct Answer</label>
          <input v-model="correctAnswers" placeholder="Correct">
        </sui-form-field>
      </sui-form>
    </div>
    <div class="submit">
      <button
          class="btn btn-primary edit-btn"
          :style="returnPrimaryButtonStyle"
          style="float: right;"
          data-toggle="tooltip"
          data-placement="bottom"
          title="Add"
          @click="writeQuestion()"
      >Add Question</button>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex';
import LoadingLayer from './LoadingLayer.vue';

export default {
  components: { LoadingLayer },
  data() {
    return {
      numberOfAnswers: 4,
      questionText: '',
      answerTexts: [],
      baseLabel: 65,
      numberOfVariables: 0,
      correctAnswers: '',
      variableTexts: [],
      variableTypes: [],
    };
  },
  mounted() {
    this.variableTypes = [{text: 'Integer Range', value: 0}, {text: 'Decimal Range', value: 1}, {text: 'Discrete Set', value: 2}]; 
    this.updateAnswers();
    this.updateVariables();
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  props: {
    select: {
      type: Boolean,
      required: true,
    }
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    updateAnswers() {
      let newAnswers = [];
      while(newAnswers.length < this.numberOfAnswers) {
        newAnswers.push({label: String.fromCharCode(this.baseLabel + newAnswers.length) + '.', text: '', index: newAnswers.length});
      }
      
      for(let i = 0; i < Math.min(this.answerTexts.length, this.numberOfAnswers); i++) {
        newAnswers[i].text = this.answerTexts[i].text;
      }

      this.answerTexts = newAnswers;
    },
    addAnswer() {
      this.numberOfAnswers += 1;
      this.updateAnswers();
    },
    removeAnswer() {
      this.numberOfAnswers -= 1;
      this.updateAnswers();
    },
    updateCorrect(n) {
      if(this.select) {
        this.answerTexts[n].correct = !this.answerTexts[n].correct;
      } else {
        if (this.answerTexts[n].correct) {
          this.answerTexts[n].correct = false;
        } else {
          for(let i = 0; i < this.answerTexts.length; i += 1){
            this.answerTexts[i].correct = false;
          }
          this.answerTexts[n].correct = true;
        }
      }
    },
    updateVariables() {
      let newVariables = [];
      while(newVariables.length < this.numberOfVariables) {
        newVariables.push({name: String.fromCharCode(this.baseLabel + newVariables.length), type: 0, range: ''});
      }
      
      for(let i = 0; i < Math.min(this.variableTexts.length, this.numberOfVariables); i++) {
        newVariables[i].name = this.variableTexts[i].name;
        newVariables[i].type = this.variableTexts[i].type;
        newVariables[i].range = this.variableTexts[i].range;
      }

      this.variableTexts = newVariables;
    },
    addVariable() {
      this.numberOfVariables += 1;
      this.updateVariables();
    },
    removeVariable() {
      this.numberOfVariables -= 1;
      this.updateVariables();
    },
    validate() {
      if (this.questionText == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Question text is empty.',
          duration: 10000,
        });
        return false;
      }

      for(let i = 0; i < this.variableTexts.length; i += 1) {
        if(this.variableTexts[i].name == '') {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Error',
            message: 'One or more variable names are not defined.',
            duration: 10000,
          });
          return false;
        }

        if(this.variableTexts[i].range == '') {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Error',
            message: 'One or more variable ranges are not defined.',
            duration: 10000,
          });
          return false;
        }
      }

      let questionTokens = this.questionText.split(' ');
      for(let i = 0; i < questionTokens.length; i += 1) {
        if(questionTokens[i].substring(0,2) == '${' && questionTokens[i].substring(questionTokens[i].length-1) == '}') {
          let potentialVarName = questionTokens[i].substring(2, questionTokens[i].length-1);
          let valid = false;
          for(let j = 0; j < this.variableTexts.length; j += 1) {
            if (this.variableTexts[j].name == potentialVarName) {
              valid = true;
              break;
            }
          }
          if (!valid) {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Error',
              message: 'No variable named \'' + potentialVarName + '\' as used in the question text.',
              duration: 10000,
            });
            return false;
          }
        }
      }

      for(let i = 0; i < this.answerTexts.length; i += 1) {
        if(this.answerTexts[i].text == '') {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Error',
            message: 'One or more answers are not defined.',
            duration: 10000,
          });
          return false;
        }

        let answerTokens = this.answerTexts[i].text.split(' ');
        for(let k = 0; k < answerTokens.length; k += 1) {
          if(answerTokens[k].substring(0,2) == '${' && answerTokens[k].substring(answerTokens[k].length-1) == '}') {
            let potentialVarName = answerTokens[k].substring(2, answerTokens[k].length-1);
            let valid = false;
            for(let j = 0; j < this.variableTexts.length; j += 1) {
              if (this.variableTexts[j].name == potentialVarName) {
                valid = true;
                break;
              }
            }
            if (!valid) {
              this.openToast();
              this.setToastInfo({
                type: 'error',
                title: 'Error',
                message: 'No variable named \'' + potentialVarName + '\'. This is used in answer \'' + this.answerTexts[i].label + '\'',
                duration: 10000,
              });
              return false;
            }
          }
        }
      }

      if (this.correctAnswers == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'No correct answers defined.',
          duration: 10000,
        });
        return false;
      }

      let answersTokens = this.correctAnswers.split(' ');
      console.log(answersTokens);
      if(!this.select && answersTokens.length > 1) {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Only define one correct answer for Multiple Choice questions.',
          duration: 10000,
        });
        return false;
      }

      for(let i = 0; i < answersTokens.length; i += 1) {
        if(answersTokens[i].length > 1) {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Error',
            message: 'Answers only have single character labels. Seperate correct answers with spaces.',
            duration: 10000,
          });
          return false;
        }

        let potentialLabel = answersTokens[i].substring(0, 1).toUpperCase();
        let valid = false;
        for(let j = 0; j < this.answerTexts.length; j += 1) {
          if(potentialLabel == this.answerTexts[j].label.substring(0,1)) {
            valid = true;
            break;
          }
        }
        if(!valid) {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Error',
            message: 'No answer labeled \'' + potentialLabel + '\'.',
            duration: 10000,
          });
          return false;
        }
      }

      return true;
    },
    writeQuestion() {
      if(this.validate()){
        this.openToast();
        this.setToastInfo({
          type: 'success',
          title: 'Success',
          message: 'Added question',
          duration: 10000,
        });
      }
    }
  },
};
</script>

<style scoped>
.question {
  display: grid;
  grid-template-areas:
      'description'
      'questionText'
      'variables'
      'variableButtons' 
      'answers'
      'buttons'
      'correct' 
      'submit';
    grid-template-rows: auto auto auto auto auto auto auto;
}
.description {
  grid-area: description;
  padding-left: 10pt;
  padding-right: 10pt;
  padding-top: 10pt;
  padding-bottom: 10pt;
}
.questionText {
  grid-area: questionText;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.variables {
  grid-area: variables;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.variable {
  grid-area: variable;
  display: grid;
  grid-template-areas:
    'name type range';
  grid-template-columns: 2fr 2fr 6fr;
}
.name {
    grid-area: name;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.type {
    grid-area: type;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.range {
    grid-area: range;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.variableButtons {
  grid-area: variableButtons;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.answers {
  grid-area: answers;
    padding-left: 10pt;
    padding-right: 10pt;
}
.answer {
  grid-area: answer;
  display: grid;
  grid-template-areas:
      'label text';
    grid-template-columns: 1fr 20fr;
}
.submit {
      grid-area: submit;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.label {
    grid-area: label;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
    align-self: center;
}
.text {
    grid-area: text;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.correct {
  grid-area: correct;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.buttons {
  grid-area: buttons;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
</style>