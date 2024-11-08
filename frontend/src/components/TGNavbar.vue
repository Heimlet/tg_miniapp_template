<template>
  <div class="container">
    <div class="row align-items-center justify-content-between">
      <div class="col-8">
        <div class="col-12">
          <div class="user-profile" @click="goToProfilePage">
            <Chip icon="pi pi-chevron-down" :label="user?.profile?.fullname"/>
          </div>
        </div>
      </div>
      <div class="col-auto align-self-end">
        <div class="main-menu-button">
          <router-link :to="{name: 'Home'}">
            <Button outlined class="border-2">
              <LogoIcon width="25.000000pt" height="25.000000pt" fillColor="var(--p-primary-500)"/>
            </Button>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useRouter} from 'vue-router';
import {computed} from "vue";
import {useStore} from "vuex";
import LogoIcon from "@/components/icons/LogoIcon.vue"

export default {
  components: {
    LogoIcon,
  },
  setup() {
    const store = useStore();
    const router = useRouter();
    const user = computed(() => store.getters['auth/user']);

    const goToProfilePage = () => {
      router.push({name: 'Profile'});
    };

    return {
      goToProfilePage,
      user,
    }

  }
}
</script>
<style lang="scss" scoped>
.container {
  max-width: 100%;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  padding-right: 8px;
}

.user-profile .p-chip {
  max-width: 100%;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.main-menu-button {
  self-align: flex-end;
}
</style>