<template>
  <div class="question">
  <div class="description">
      <h3>Code Execution</h3>
      <p>This type of question will have a student determine the result of operations on a data structure. This requires the uploading of two .java files, one with a reference implementation of the data structure with the requisite operations, and another that runs a suite of tests by taking a list of operations to be performed from the command line.</p>
      
  </div>
    <sui-form class="questionText">
        <sui-form-field>
          <label>Question Text</label>
          <input v-model="identity" placeholder="Question Text" type="text">
        </sui-form-field>
    </sui-form>
    <sui-form class="operations">
      <sui-form-field>
        <label style="padding-left: 10pt">Define Operations</label>
        <div class="operation" v-for="(item, index) in OperationTexts" :key="index">
          <input v-model="item.text" placeholder="Operation">
        </div>
      </sui-form-field>
    </sui-form>
    <div class="buttons">
    <center>
      <button
          :class="numberOfOperation <= 0 ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                  :disabled="numberOfOperation <= 0 ? true : false"
                  :style="numberOfOperation <= 0 ? '' : returnPrimaryButtonStyle"
          data-toggle="tooltip"
          data-placement="bottom"
          title="RemoveOperation"
          @click="removeOperation()"
      >Remove Operation</button>
      <button
          :class="numberOfOperation >= 10 ? 'btn btn-disabled' : 'btn btn-primary edit-btn'"
                  :disabled="numberOfOperation >= 10 ? true : false"
                  :style="numberOfOperation >= 10 ? '' : returnPrimaryButtonStyle"
          data-toggle="tooltip"
          data-placement="bottom"
          title="AddOperation"
          @click="addOperation()"
      >Add Operation</button>
    </center>
    <div class="upload">
      <center>
        <div>
          <label>Upload Implementation: </label>
          <input type="file" id="file" ref="implementation" v-on:change="handleImplementationUpload()"/>
        </div>
        <div>
          <label>Upload Test Harness: </label>
          <input type="file" id="file" ref="harness" v-on:change="handleHarnessUpload()"/>
        </div>
      </center>
    </div>
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
import axios from 'axios';
import { mapGetters, mapState, mapMutations } from 'vuex';
import { API_URL } from '@/constants';

export default {
  data() {
    return {
      numberOfOperation: 0,
      identity: '',
      OperationTexts: [],
      implementation: '',
      harness: '',
    };
  },
  mounted() {
    this.updateOperation();
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  props: {
    quiz: {
      type: Number,
      required: true,
    },
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    updateOperation() {
      let newOperation = [];
      while(newOperation.length < this.numberOfOperation) {
        newOperation.push({text: '', index: newOperation.length});
      }
      
      for(let i = 0; i < Math.min(this.OperationTexts.length, this.numberOfOperation); i++) {
        newOperation[i].text = this.OperationTexts[i].text;
      }

      this.OperationTexts = newOperation;
    },
    addOperation() {
      this.numberOfOperation += 1;
      this.updateOperation();
    },
    removeOperation() {
      this.numberOfOperation -= 1;
      this.updateOperation();
    },
    handleImplementationUpload(){
      this.implementation = this.$refs.implementation.files[0];
    },
    handleHarnessUpload(){
      this.harness = this.$refs.harness.files[0];
    },
    validate() {
      if (this.identity == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Didn\'t define a question text.',
          duration: 10000,
        });
        return false;
      }

      if (this.numberOfOperation == 0) {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Didn\'t define any operations.',
          duration: 10000,
        });
        return false;
      } else {
        for(let i = 0; i < this.numberOfOperation; i += 1) {
          if(this.OperationTexts[i].text == '') {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Error',
              message: 'One or more operations are not defined.',
              duration: 10000,
            });
            return false;
          }
        }
      }

      if (this.implementation == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Didn\'t provide an implementation.',
          duration: 10000,
        });
        return false;
      }

      if (this.harness == '') {
        this.openToast();
        this.setToastInfo({
          type: 'error',
          title: 'Error',
          message: 'Didn\'t provide a test harness.',
          duration: 10000,
        });
        return false;
      }
      return true;
    },
    writeQuestion() {
      if(this.validate()){
        let questionData = {
          'quiz-questions': [{
            pk: 'None',
            quiz: this.quiz,
            question_type: 4,
            answered_correct: 0,
            answered_total: 0,
            question_parameters: JSON.stringify({
              identity: this.identity,
              operations: this.OperationTexts,
              implementation: this.identity + '_implementation',
              harness: this.identity + '_harness',
            })
          }]
        };
        axios.post(`${API_URL}/quiz-questions/`,
          questionData,
          {
            headers: {
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then((response)=> {
          if(response.data.status == '200 - OK') {   
            axios.get(`${API_URL}/quiz-questions/`,
              {
                params: {
                  quiz: this.quiz,
                  mode: 'practice'
                },
                headers: {
                  Authorization: `Bearer ${this.profile.id_token}`
                },
              }
            ).then((response) => {
              this.question = response.data.result[response.data.result.length - 1].pk;

              let formData = new FormData();
              formData.append('implementation', this.implementation);
              formData.append('harness', this.harness); 
              axios.post(`${API_URL}/questionFileUpload/${this.question}`,
                formData,
                {
                  headers: {
                    'Content-Type': 'multipart/form-data',
                    Authorization: `Bearer ${this.profile.id_token}`
                  },
                }
              ).then((response) => {
                if(response.data.status == '200 - OK') {
                  this.openToast();
                  this.setToastInfo({
                    type: 'success',
                    title: 'Successful Creation',
                    message: 'Question successfully added',
                    duration: 5000,
                  });
                  this.$emit('onClose');
                }
              });
            });
          }
          else {
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Creation Error',
              message: `${response.data.errors}`,
              duration: 10000,
            });
          }
        }).catch(function(){
          console.log('Question writing failure');
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
      'operations'
      'buttons' 
      'upload'
      'submit';
    grid-template-rows: auto auto auto auto auto auto;
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
.operations {
  grid-area: operations;
  padding-left: 10pt;
  padding-right: 10pt;
  padding-top: 10pt;
  padding-bottom: 10pt;
}
.operation {
  grid-area: operation;
  padding-left: 10pt;
  padding-right: 10pt;
  padding-top: 10pt;
  padding-bottom: 10pt;
}
.submit {
  grid-area: submit;
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
.upload {
  grid-area: upload;
  padding-left: 10pt;
  padding-right: 10pt;
  padding-top: 10pt;
  padding-bottom: 10pt;
}
</style>