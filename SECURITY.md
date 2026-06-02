# Security Policy

Merci d'avoir signalé un problème de sécurité. Pour signaler une vulnérabilité, merci d'utiliser les GitHub Security Advisories du dépôt ou d'envoyer un message privé au propriétaire du dépôt.

Procédure de signalement
- Ouvrir une [Security Advisory](https://docs.github.com/en/code-security/security-advisories/about-security-advisories) sur GitHub pour ce dépôt.
- Alternativement, ouvrir une issue en marquant le libellé `security` (privée si nécessaire) et indiquer clairement les étapes pour reproduire.

Réponse
- Nous nous efforçons de reconnaître la réception d'un signalement en moins de 48 heures et de publier un correctif ou un avis dans un délai raisonnable.

Divulgation responsable
- Ne publiez pas publiquement les détails techniques d'une vulnérabilité avant qu'un correctif soit disponible.

Configuration GitHub recommandée
- Activez la protection de branche pour `main`.
- Exigez les revues de pull request avant fusion.
- Exigez l'approbation des code owners (`.github/CODEOWNERS`).
- Exigez les vérifications de statut suivantes avant fusion :
  - `run-script` (CI)
  - `analyze` (CodeQL)
- Exigez que les GitHub Actions utilisent des workflows vérifiés et un `PYPI_API_TOKEN` pour les publications.
- Activez le scanner de secrets GitHub si disponible pour éviter les fuites de clés dans le code.
