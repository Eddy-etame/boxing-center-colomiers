import type { APIRoute } from 'astro';

/**
 * Relais du formulaire vers Inlet.
 *
 * Inlet attend du JSON et une preuve de travail (SHA-256 à résoudre). Un
 * <form> HTML natif ne sait faire ni l'un ni l'autre : il envoie du
 * form-urlencoded, sans calcul préalable. On reçoit donc le POST natif ici,
 * on résout la preuve côté serveur, on relaie en JSON, puis on redirige.
 *
 * Deux bénéfices, en plus de faire marcher le formulaire :
 *   — le formulaire fonctionne sans JavaScript, ce qui n'était pas possible
 *     en appelant Inlet directement depuis le navigateur ;
 *   — l'appel part du serveur, donc CORS ne s'applique pas. L'autorisation
 *     du domaine chez Inlet reste une ceinture de sécurité, pas une condition.
 */
export const prerender = false;

const INLET = 'https://inlett.vercel.app';
const FORMULAIRE = '615a1cc9-3025-427f-992d-1b6a9ea0a080';

/** Où l'on renvoie le visiteur. Le domaine final le résout en /merci/. */
const SUCCES = '/merci/';
const ECHEC = '/contact/?erreur=1#formulaire';

type Defi = { challenge: string; difficulty?: number; timestamp?: number | string };

/**
 * Résout le défi : on cherche un nonce dont le SHA-256 commence par N zéros.
 * Borné à 5 millions d'essais pour ne jamais bloquer une requête ; en
 * pratique une difficulté de 4 se résout en quelques milliers d'itérations.
 */
async function resoudre(defi: string, difficulte: number): Promise<string | null> {
  const prefixe = '0'.repeat(Math.max(0, difficulte));
  const encodeur = new TextEncoder();
  for (let nonce = 0; nonce < 5_000_000; nonce++) {
    const empreinte = await crypto.subtle.digest('SHA-256', encodeur.encode(defi + nonce));
    const hex = [...new Uint8Array(empreinte)].map((b) => b.toString(16).padStart(2, '0')).join('');
    if (hex.startsWith(prefixe)) return String(nonce);
  }
  return null;
}

const texte = (v: FormDataEntryValue | null, max = 4000) =>
  typeof v === 'string' ? v.trim().slice(0, max) : '';

export const POST: APIRoute = async ({ request, redirect }) => {
  let donnees: FormData;
  try {
    donnees = await request.formData();
  } catch {
    return redirect(ECHEC, 303);
  }

  // Pot de miel : rempli, c'est un robot. On répond comme si tout allait
  // bien — un robot ne doit pas apprendre qu'il a été repéré.
  if (texte(donnees.get('_gotcha'))) return redirect(SUCCES, 303);

  const prenom = texte(donnees.get('prenom'), 80);
  const nom = texte(donnees.get('nom'), 80);
  const email = texte(donnees.get('email'), 160);
  const telephone = texte(donnees.get('telephone'), 40);
  const activite = texte(donnees.get('activite'), 80);
  const club = texte(donnees.get('club'), 80);
  const secteur = texte(donnees.get('secteur'), 120);
  const message = texte(donnees.get('message'), 4000);
  const parcours = texte(donnees.get('parcours'), 400);

  // Validation serveur : elle fait autorité, quoi que fasse le navigateur.
  const manque = !prenom || !email || !message || !/^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(email);
  if (manque) return redirect(ECHEC, 303);

  const charge: Record<string, string> = {
    name: [prenom, nom].filter(Boolean).join(' '),
    email,
    telephone,
    activite_recherchee: activite,
    club_souhaite: club || secteur,
    message,
    // Le parcours suivi sur le site part avec la demande : celui qui répond
    // sait déjà d'où vient la personne et ce qu'elle cherche.
    parcours_sur_le_site: parcours,
    origine: 'boxingcenter-colomiers.fr',
    _lang: 'fr',
    _gotcha: '',
  };

  try {
    // La preuve de travail est facultative côté serveur : si le défi n'est
    // pas joignable, on tente l'envoi sans. Un formulaire ne doit jamais
    // échouer à cause d'une étape anti-robot qu'on s'impose à soi-même.
    const rep = await fetch(`${INLET}/api/challenge`, { headers: { accept: 'application/json' } });
    if (rep.ok) {
      const defi = (await rep.json()) as Defi;
      if (defi?.challenge) {
        const nonce = await resoudre(defi.challenge, Number(defi.difficulty ?? 4));
        if (nonce !== null) {
          charge.pow_challenge = defi.challenge;
          charge.pow_timestamp = String(defi.timestamp ?? Date.now());
          charge.pow_nonce = nonce;
        }
      }
    }
  } catch {
    /* on continue sans preuve */
  }

  try {
    const envoi = await fetch(`${INLET}/api/submit/${FORMULAIRE}`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(charge),
    });
    if (!envoi.ok) {
      console.error('Inlet a refusé la soumission :', envoi.status, await envoi.text());
      return redirect(ECHEC, 303);
    }
  } catch (e) {
    console.error('Inlet injoignable :', e);
    return redirect(ECHEC, 303);
  }

  return redirect(SUCCES, 303);
};

/** Un GET sur l'endpoint n'a pas de sens : on renvoie au formulaire. */
export const GET: APIRoute = ({ redirect }) => redirect('/contact/', 303);
