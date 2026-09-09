"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, type SubmitEvent } from "react";
import { useAuth } from "@/context/authContext";

type AuthFormProps = {
  mode: "login" | "register";
};

export function AuthForm({ mode }: AuthFormProps) {
  const { login, register } = useAuth();
  const router = useRouter();

  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [greeting, setGreeting] = useState("");
  const [pepTalk, setPepTalk] = useState("");

  const isRegister = mode === "register";

  useEffect(() => {
    const greetings = ["Hello there", "Watch anything good recently?", "Greetings movie dork", "Why so serious?", "You are so fetch", "Whoa, this is heavy"];
    const pepTalks = ["Less scrolling, More watching", "Always watch through the credits", "Keep it indie", "May the force be with you", "It's a trap!", "You can't handle the truth!"];

    setGreeting(greetings[Math.floor(Math.random() * greetings.length)]);
    setPepTalk(pepTalks[Math.floor(Math.random() * pepTalks.length)]);
  }, []);

  async function handleSubmit(e: SubmitEvent) {
    e.preventDefault();
    setError("");

    try {
      if (isRegister) {
        await register(username, email, password);
      } else {
        await login(email, password);
      }
      router.push("/feed");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 bg-white w-[400px] h-[450px] p-4 rounded-2xl flex flex-col justify-center text-slate-500">
      {error && <p className="text-red-600">{error}</p>}
      <h1 className="text-center text-xl font-bold pb-4">{greeting}</h1>

      {isRegister && (
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full border p-2 rounded-md"
          required
        />
      )}

<input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full border p-2 rounded-md"
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full border p-2 rounded-md"
      />

      <button type="submit" className="w-full bg-slate-500 py-2 text-white rounded-md">
        {isRegister ? "Join us" : "Log in"}
      </button>

      <Link
        href={isRegister ? "/login" : "/register"}
        className="text-center italic underline"
      >
        {isRegister ? "Already one of us?" : "Maybe you're new here?"}
      </Link>

      <h1 className="text-center text-xl font-bold">{pepTalk}</h1>
    </form>
  );
}