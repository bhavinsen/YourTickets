<template>
  <v-container
    class="fill-height"
    fluid
  >

    <v-dialog
        v-model="dialog"
        max-width="400"
        persistent
    >
      <v-card>
        <v-card-title class="headline">
          Login
        </v-card-title>

        <v-card-text>
          <v-text-field label="Username" v-model="account.username"></v-text-field>
          <v-text-field label="Password" type="password" v-model="account.password"></v-text-field>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
              color="green darken-1"
              @click="login"
          >
            Login
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>


// import Api from "@/service/Api";
// import axios from 'axios'

export default {
  name: 'Login',
  mounted(){

  },
  methods:{
    login(){
      // console.log(this.$cookies.get('csrftoken'))
      this.$store.dispatch('account/login', this.account)
      .then((response) => {
        localStorage.t = response.data.token;

        this.$store.cache.dispatch('account/load')
        this.$store.dispatch('event/loadEvents')
        this.$router.push({'name': 'home'})
      })
      .finally(() => this.loading = false)
    }
  },
  data: () => ({
    dialog: true,
    account:{
      username:'',
      password:''
    }

  })

}
</script>
