<template>
  <div class="question">
    <div class="description">
      <h3>Code Implementation</h3>
      <p>This type of question will have a student a section of code from a implementation of a data structure. This requires the uploading of two .java files, one with a reference implementation with formatted comments (described below), and another that runs a suite of tests using that implementation.</p>
      <h3>Format</h3>
      <p>Upload a .java file containing the tags below to have students implement their own lines of code.</p>
      <ul>
        <li>//$method {method_name} - on the line above a method will ask a student to implement the whole method.</li>
        <li>//$line {method_name}   - on the same line as a line of code will ask a student to implement that line of code.</li>
      </ul>
    </div>
    <sui-form class="questionText">
        <sui-form-field>
          <label>What is this an implementation of?</label>
          <input v-model="identity" placeholder="Implementation" type="text">
        </sui-form-field>
    </sui-form>
    <div class="buttons">
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
    <div class="submit">
      <sui-form-field>
        <button
            class="btn btn-primary edit-btn"
            :style="returnPrimaryButtonStyle"
            style="float: right;"
            data-toggle="tooltip"
            data-placement="bottom"
            title="Add"
            @click="writeQuestion()"
        >Add Question</button>
      </sui-form-field>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapState, mapMutations } from 'vuex';

export default {
  data() {
    return {
      identity: '',
      implementation: '',
      harness: '',
    };
  },
  mounted() {
  },
  computed: {
    ...mapState('auth', ['profile']),
    ...mapGetters('settings', ['returnPrimaryButtonStyle']),
  },
  props: {
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
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
          message: 'Didn\'t specify what this question is an implementation of.',
          duration: 10000,
        });
        return false;
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
      'buttons' 
      'submit';
    grid-template-rows: auto auto auto auto;
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
.aswers {
  grid-area: answers;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
.answer {
  grid-area: answer;
  display: grid;
  grid-template-areas:
      'label text correct';
    grid-template-columns: 1fr 20fr 3fr;
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
    align-self: center;
}
.buttons {
  grid-area: buttons;
    padding-left: 10pt;
    padding-right: 10pt;
    padding-top: 10pt;
    padding-bottom: 10pt;
}
</style>