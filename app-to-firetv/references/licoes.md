# Lições que originaram esta skill (não repetir)

1. **Nunca montar binários Android à mão** (DEX, AndroidManifest binário, resources.arsc, bloco de assinatura). APKs gerados assim instalam com a assinatura v2 corrompida ("O aplicativo não foi instalado") ou instalam e fecham ao abrir. Use sempre o toolchain padrão: apktool (smali + aapt2) e uber-apk-signer (zipalign + apksigner), pelo `scripts/firetv_build.py`.
2. **Layout em pixels fixos estoura na TV.** A Fire TV expõe ao WebView uma viewport de cerca de 960x540 (ou 1280x720) px CSS, e muitas TVs cortam as bordas (overscan). Desenhe sempre num palco de tamanho fixo e escale com `transform: scale()` para caber numa área segura com margem ajustável.
3. **Link de pasta do Drive não serve para o Downloader.** É preciso o link direto do arquivo, compartilhado como "Qualquer pessoa com o link".
4. **Manter a mesma keystore** em todas as versões e aumentar o `versionCode` a cada build. Assim o app atualiza por cima, sem desinstalar.
