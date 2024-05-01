
<template>
  <v-app-bar
    app
    color="blue darken-3"
    dark
  >
    <v-app-bar-nav-icon @click.stop="togglenav"></v-app-bar-nav-icon>
    <v-toolbar-title
      style="width: 300px"
      class="ml-0 pl-4"
      to="/"
    >
      <v-img
        alt="Yourtickets"
        class="shrink mt-1 hidden-sm-and-down"
        contain
        min-width="100"
        src="/logo.png"
        width="200"
      />
    </v-toolbar-title>

    <v-spacer></v-spacer>

<!--    <v-btn icon>-->
<!--      <v-icon>mdi-bell</v-icon>-->
<!--    </v-btn>-->
    <v-switch
        v-model="$vuetify.theme.dark"
        hint="This toggles the global state of the Vuetify theme"
        inset
        label="Dark/Light mode"
        persistent-hint
      ></v-switch>
    <v-menu
        bottom
        left
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn icon large
               v-bind="attrs"
               v-on="on"
        >
          <v-icon>mdi-account</v-icon>
        </v-btn>
      </template>

      <v-list>
        <v-list-item :to="{name:'account'}">
          <v-list-item-icon>
            <v-icon>mdi-account</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Account settings</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-divider></v-divider>
        <v-list-item>

          <v-list-item-content>
            <v-btn color="primary" @click="logout" text block >Logout</v-btn>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>


  </v-app-bar>
</template>
<script>
  export default {
    name: 'appbar',
    methods: {
      togglenav() {
        this.$store.commit('layout/navopen', !this.$store.state.layout.navopen)
      },
      test(){
        console.log('yeah')
      },
      logout(){
        localStorage.removeItem('t')
        this.$router.push({name:'login'})
      }
    },
    data: () => ({

      })
  }
</script>
