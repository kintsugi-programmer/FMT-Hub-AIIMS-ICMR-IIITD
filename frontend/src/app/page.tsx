"use client";
import { useState, ChangeEvent, FormEvent } from "react";
import axios from "axios";

interface FormDataState {
    text1: string;
    text2: string;
    text3: string;
    file: File | null;
}

export default function Home() {
    const [formData, setFormData] = useState<FormDataState>({
        text1: "",
        text2: "",
        text3: "",
        file: null,
    });

    const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files.length > 0) {
            setFormData({ ...formData, file: e.target.files[0] });
        }
    };

    const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const data = new FormData();
        data.append("text1", formData.text1);
        data.append("text2", formData.text2);
        data.append("text3", formData.text3);

        if (formData.file) {
            data.append("file", formData.file);
        }

        try {
            const response = await axios.post("http://localhost:8000/submit-form/", data, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            alert(response.data.message);
        } catch (error) {
            console.error("Error submitting form", error);
        }
    };

    return (
        <div className="p-6 max-w-lg mx-auto">
            <h1 className="text-xl font-bold mb-4">Google Forms Clone</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="text"
                    name="text1"
                    placeholder="Text 1"
                    value={formData.text1}
                    onChange={handleChange}
                    className="block w-full p-2 border"
                    required
                />
                <input
                    type="text"
                    name="text2"
                    placeholder="Text 2"
                    value={formData.text2}
                    onChange={handleChange}
                    className="block w-full p-2 border"
                    required
                />
                <input
                    type="text"
                    name="text3"
                    placeholder="Text 3"
                    value={formData.text3}
                    onChange={handleChange}
                    className="block w-full p-2 border"
                    required
                />
                <input
                    type="file"
                    name="file"
                    accept="image/*,video/*,application/pdf"
                    onChange={handleFileChange}
                    className="block w-full p-2 border"
                />
                <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
                    Submit
                </button>
            </form>
        </div>
    );
}
