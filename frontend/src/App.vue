<template>
  <div id="main" :style="{ paddingBottom: keyboardPadding }">
    <div class="container">

      <div class="row mb-3 align-items-center mw-100">
        <ADANavbar v-if="is_telegram_client && is_telegram_api_updated && isLoggedIn"/>
      </div>
      <div class="row mt-2">
        <router-view v-if="is_telegram_client && is_telegram_api_updated && isLoggedIn"/>
        <div v-else>
          <div>{{ isLoggedIn ? '⚠️' : '' }}</div>
          <RequirementsMessage
              :is-telegram-client="is_telegram_client"
              :is-telegram-api-updated="is_telegram_api_updated"
              :TWA="TWA"
          />
          <div class="container">
            <div class="row align-items-center">
              <div class="col-12">
                <!-- Skeleton for User Profile Chip -->
                <Skeleton width="100%" height="5rem" class="mb-2"></Skeleton>
              </div>
            </div>
            <div class="row mt-3">
              <Skeleton width="100%" height="3rem" class="mb-2"></Skeleton>
              <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
              <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
              <Skeleton width="100%" height="2rem" class="mb-2"></Skeleton>
            </div>
          </div>
        </div>
      </div>
      <div class="row mt-1 align-items-center bottom-logo">
        <LogoIcon fillColor="var(--p-background-highlight)"/>
      </div>
    </div>
  </div>
</template>

<script>
import {computed, inject, onMounted, provide, ref} from 'vue';
import {useStore} from 'vuex';
import {useRouter} from "vue-router";
import RequirementsMessage from "@/components/RequirementsMessage.vue";
import ADANavbar from "@/components/TGNavbar.vue";
import LogoIcon from "@/components/icons/LogoIcon.vue";

export default {
  name: 'App',
  components: {LogoIcon, ADANavbar, RequirementsMessage},
  setup() {
    const appTitle = ref('');
    const globalState = inject('globalState');
    const store = useStore();
    const router = useRouter();
    const TWA = ref(null);
    const is_telegram_client = ref('');
    const is_telegram_api_updated = ref('');
    const keyboardPadding = ref(0);

    appTitle.value = import.meta.env.VITE_APP_TITLE
    const verifyAuthentication = async (TWAInstance) => {
      await store.dispatch('auth/fetchUser', {TWA: TWAInstance});
    };

    const isLoggedIn = computed(() => store.getters['auth/isLoggedIn']);


    const updateKeyboardPadding = () => {
      const originalHeight = document.documentElement.clientHeight;
      const onResize = () => {
        const newHeight = document.documentElement.clientHeight;
        const heightDifference = originalHeight - newHeight;
        keyboardPadding.value = heightDifference > 100 ? `${heightDifference + 100}px` : '0px';
      };

      window.addEventListener('resize', onResize);
    };

    onMounted(async () => {
      // Input lost focus bugfix
      document.addEventListener('click', function (e) {
        if (!e.target.matches('input, textarea')) {
          document.activeElement.blur();
        }
      }, false);

      if (window.Telegram && window.Telegram.WebApp && window.Telegram.platform != 'unknown') {
        provide('TWA', window.Telegram.WebApp);
        TWA.value = window.Telegram.WebApp;
        is_telegram_client.value = true;

        const requiredApiVersion = import.meta.env.VITE_WEB_APP_MIN_VERSION;
        is_telegram_api_updated.value = window.Telegram.WebApp.isVersionAtLeast(requiredApiVersion);
      } else {
        is_telegram_client.value = false;
        is_telegram_api_updated.value = false;
      }

      const setTheme = function () {
        TWA.value.colorScheme && TWA.value.colorScheme === 'light' ? document.documentElement.classList.remove("tg-miniapp-dark") : document.documentElement.classList.add("tg-miniapp-dark");
      }

      setTheme();

      TWA.value.onEvent('themeChanged', function () {
        setTheme();
      })

      // await new Promise(r => setTimeout(r, 500));

      if (is_telegram_client.value && is_telegram_api_updated.value) {
        await verifyAuthentication(window.Telegram.WebApp);
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.BackButton.onClick(() => {
          router.back();
        })
      }

      updateKeyboardPadding();
    });

    return {
      appTitle,
      globalState,
      isLoggedIn,
      is_telegram_client,
      is_telegram_api_updated,
      TWA,
      keyboardPadding,
    }
  },
};
</script>

<style scoped>
#main {
  /*https://stackoverflow.com/questions/1165497/how-to-prevent-text-from-overflowing-in-css*/
  word-wrap: break-word;
}

.bottom-logo {
  opacity: 15%;
  padding: 15px;
}
</style>
