.class public L__PKGPATH__/MainActivity$Client;
.super Landroid/webkit/WebViewClient;
.source "MainActivity.java"

.field private final activity:L__PKGPATH__/MainActivity;

.method public constructor <init>(L__PKGPATH__/MainActivity;)V
    .registers 2
    invoke-direct {p0}, Landroid/webkit/WebViewClient;-><init>()V
    iput-object p1, p0, L__PKGPATH__/MainActivity$Client;->activity:L__PKGPATH__/MainActivity;
    return-void
.end method

.method public shouldOverrideUrlLoading(Landroid/webkit/WebView;Ljava/lang/String;)Z
    .registers 4
    if-eqz p2, :no
    const-string v0, "__SCHEME__://sair"
    invoke-virtual {p2, v0}, Ljava/lang/String;->startsWith(Ljava/lang/String;)Z
    move-result v0
    if-eqz v0, :no
    iget-object v0, p0, L__PKGPATH__/MainActivity$Client;->activity:L__PKGPATH__/MainActivity;
    invoke-virtual {v0}, L__PKGPATH__/MainActivity;->finish()V
    const/4 v0, 0x1
    return v0
    :no
    const/4 v0, 0x0
    return v0
.end method
