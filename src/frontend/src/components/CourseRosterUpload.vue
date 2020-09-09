<template>
  <div class="container">
    <div class="large-12 medium-12 small-12 cell" style="padding:10px">
      <h3>Upload course roster</h3>
      <p>This upload will create student accounts and add them to the roster. CSV Schema: email, firstname, lastname, username</p>
      <label>
        <input type="file" id="file" ref="file" v-on:change="handleFileUpload()"/>
      </label>
      <button v-on:click="submitFile()">Upload</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { mapGetters, mapMutations } from 'vuex';
import { API_URL } from '@/constants';
export default {
  /*
  Defines the data used by the component
  */
  data(){
    return {
      file: ''
    };
  },
  props: {
    courseId: {
      type: String,
      required: true,
    }
  },
  computed: {
    ...mapState('auth', ['profile']),
  },
  methods: {
    ...mapMutations('toast', ['openToast', 'setToastInfo']),
    /*
    Submits the file to the server
    */
    submitFile(){
      /*
      Initialize the form data
      */
      let formData = new FormData();
      /*
      Add the form data we need to submit
      */
      formData.append('file', this.file);
      formData.append('token', this.profile.id_token);
      /*
      Make the request to the POST /single-file URL
      */
      axios
        .post( `${ API_URL }/courseRosterUpload/${ this.courseId }/`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              Authorization: `Bearer ${this.profile.id_token}`
            }
          }
        ).then(result => {
          if(result.data.ok){
            this.openToast();
            this.setToastInfo({
              type: 'success',
              title: 'Successful Upload',
              message: 'Students added to roster',
              duration: 5000,
            });
          }else{
            this.openToast();
            this.setToastInfo({
              type: 'error',
              title: 'Uploading Error',
              message: `${result.data.errors}`,
              duration: 10000,
            });
          }
        })
        .catch(err => {
          this.openToast();
          this.setToastInfo({
            type: 'error',
            title: 'Uploading Error',
            message: `${err.response}`,
            duration: 10000,
          });
        });
    },
    /*
      Handles a change on the file upload
    */
    handleFileUpload(){
      this.file = this.$refs.file.files[0];
    }
  } 
};
</script>